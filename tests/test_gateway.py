"""Adversarial boundary tests and real loopback transport failures."""
import copy
from concurrent.futures import ThreadPoolExecutor
import http.client
import json
from pathlib import Path
import tempfile
import unittest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from aiegateway.adapter import LoopbackAdapter
from aiegateway.contracts import Denied, canonical, digest, parse_json
from aiegateway.engine import Engine
from aiegateway.fixtures import environment, sample_policy
from aiegateway.http import BoundedServer, gateway_handler
from aiegateway.identity import Principal
from aiegateway.policy import admit_policy, sign_policy
from aiegateway.store import Store

REQUEST = {"use_case": "knowledge-assistant", "prompt": "Summarize the procedure.", "max_output_bytes": 256}
ACTION = {"use_case": "site-maintenance", "tool": "maintenance.schedule",
          "arguments": {"asset": "asset-a", "window": "day"}}


class Clock:
    def __init__(self):
        self.now = 1795046400  # Fixed synthetic clock: 2026-11-19 00:00 UTC.
    def __call__(self):
        return self.now


class GatewayCases(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.ctx = environment(clock=self.clock, start_http=True)
        self.e = self.ctx.__enter__()
        self.engine, self.store = self.e["engine"], self.e["store"]
        self.token = self.e["tokens"]["government"]
    def tearDown(self):
        self.ctx.__exit__(None, None, None)
    def generate(self, value=None, key="request-1", token=None):
        return self.engine.dispatch(token or self.token, "/v1/generate", value or copy.deepcopy(REQUEST), key)
    def denied(self, code, call):
        with self.assertRaises(Denied) as caught:
            call()
        self.assertEqual(caught.exception.code, code)
    def http(self, raw, extra=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.e["server"].server_port, timeout=2)
        headers = {"Authorization": "Bearer " + self.token, "Content-Type": "application/json",
                   "Idempotency-Key": "http-1"}
        headers.update(extra or {})
        conn.request("POST", "/v1/generate", raw, headers)
        response = conn.getresponse()
        result = response.status, json.loads(response.read())
        conn.close()
        return result
    def approvals(self, action=None, requester="gov-app"):
        value = {"requester": requester, "action": copy.deepcopy(action or ACTION)}
        return [self.engine.dispatch(self.e["tokens"][r], "/v1/approvals", value)["approval"]
                for r in ("reviewer-a", "reviewer-b")]
    def invoke(self, action):
        return self.engine.dispatch(self.token, "/v1/tools/invoke", action)

    def test_approved_route_is_local_despite_cheaper_external_model(self):
        result = self.generate()
        self.assertEqual(result["model"], "local-standard")
        self.assertEqual(self.e["providers"][2].calls, 0)

    def test_real_http_request_returns_security_headers(self):
        status, result = self.http(canonical(REQUEST))
        self.assertEqual(status, 200)
        self.assertEqual(result["region"], "site-a")

    def test_client_tenant_spoof_is_rejected(self):
        self.denied("invalid_fields", lambda: self.generate({**REQUEST, "tenant": "bfsi"}))
        self.assertEqual(self.e["providers"][0].calls, 0)

    def test_client_endpoint_is_rejected(self):
        self.denied("invalid_fields", lambda: self.generate({**REQUEST, "endpoint": "http://169.254.169.254/"}))

    def test_client_model_override_is_rejected(self):
        self.denied("invalid_fields", lambda: self.generate({**REQUEST, "model": "external-cheap"}))

    def test_public_label_cannot_lower_server_classification(self):
        self.engine.policy["models"]["local-standard"]["classes"] = ["public"]
        result = self.generate({**REQUEST, "classification": "public"})
        self.assertEqual(result["model"], "local-backup")

    def test_higher_classification_is_honored(self):
        for model in self.engine.policy["models"].values():
            model["classes"] = ["public", "internal"]
        self.denied("no_eligible_model", lambda: self.generate({**REQUEST, "classification": "restricted"}))

    def test_expired_identity_denied(self):
        token = self.e["identity"].issue(self.e["principals"]["government"], 1)
        self.clock.now += 2
        self.denied("invalid_credential", lambda: self.generate(token=token))

    def test_revoked_identity_cannot_replay_cached_result(self):
        self.generate()
        self.e["identity"].revoke(self.token)
        self.denied("invalid_credential", self.generate)

    def test_unknown_token_denied(self):
        self.denied("invalid_credential", lambda: self.generate(token="x" * 43))

    def test_wrong_scope_denied(self):
        self.denied("scope_denied", lambda: self.generate(token=self.e["tokens"]["reviewer-a"]))

    def test_unregistered_use_case_denied(self):
        self.denied("use_case_denied", lambda: self.generate({**REQUEST, "use_case": "unknown"}))

    def test_suspended_use_case_denied(self):
        self.engine.policy["use_cases"]["knowledge-assistant"]["state"] = "suspended"
        self.denied("use_case_not_current", self.generate)

    def test_expired_use_case_review_denied(self):
        self.engine.policy["use_cases"]["knowledge-assistant"]["review_expires"] = self.clock.now
        self.denied("use_case_not_current", self.generate)

    def test_expired_policy_denied_before_cache(self):
        self.generate()
        self.clock.now += 3600
        fresh = self.e["identity"].issue(self.e["principals"]["government"])
        self.denied("policy_not_current", lambda: self.generate(token=fresh))

    def test_retired_models_denied(self):
        for m in self.engine.policy["models"].values():
            m["state"] = "retired"
        self.denied("no_eligible_model", self.generate)

    def test_expired_model_reviews_denied(self):
        for m in self.engine.policy["models"].values():
            m["review_expires"] = self.clock.now
        self.denied("no_eligible_model", self.generate)

    def test_same_tenant_authorized_retrieval(self):
        self.assertEqual(self.generate({**REQUEST, "document_id": "gov-doc"})["model"], "local-standard")

    def test_cross_tenant_retrieval_denied(self):
        self.denied("document_access_denied", lambda: self.generate({**REQUEST, "document_id": "bank-doc"}))

    def test_document_subject_acl_denied(self):
        self.engine.documents["gov-doc"]["subjects"] = ["someone-else"]
        self.denied("document_access_denied", lambda: self.generate({**REQUEST, "document_id": "gov-doc"}))

    def test_retrieval_raises_classification(self):
        for m in self.engine.policy["models"].values():
            m["classes"] = ["public", "internal"]
        self.denied("no_eligible_model", lambda: self.generate({**REQUEST, "document_id": "gov-doc"}))

    def test_fixture_secret_in_input_denied(self):
        self.denied("fixture_sensitive_input", lambda: self.generate({**REQUEST, "prompt": "DEMO_SECRET_ABCD"}))

    def test_fixture_email_in_input_denied(self):
        self.denied("fixture_sensitive_input", lambda: self.generate({**REQUEST, "prompt": "person@example.com"}))

    def test_sensitive_output_denied_without_fallback(self):
        self.e["providers"][0].mode = "sensitive"
        self.denied("fixture_sensitive_output", self.generate)
        self.assertEqual(self.e["providers"][1].calls, 0)

    def test_timeout_falls_back_only_to_eligible_model(self):
        self.e["providers"][0].mode = "timeout"
        self.engine.adapters["provider-a"] = self.e["providers"][0].adapter(0.02)
        result = self.generate()
        self.assertEqual((result["model"], result["attempts"]), ("local-backup", 2))

    def test_outage_does_not_escape_region(self):
        for p in self.e["providers"][:2]:
            p.mode = "unavailable"
        self.denied("provider_unavailable", self.generate)
        self.assertEqual(self.e["providers"][2].calls, 0)

    def test_malformed_output_denied_without_fallback(self):
        self.e["providers"][0].mode = "malformed"
        self.denied("provider_invalid_response", self.generate)
        self.assertEqual(self.e["providers"][1].calls, 0)

    def test_oversize_output_denied(self):
        self.e["providers"][0].mode = "oversize"
        self.denied("provider_response_too_large", self.generate)

    def test_redirect_not_followed(self):
        self.e["providers"][0].mode = "redirect"
        self.assertEqual(self.generate()["model"], "local-backup")

    def test_client_bearer_is_not_forwarded(self):
        self.generate()
        seen = self.e["providers"][0].received_authorizations
        self.assertEqual(seen, ["Bearer " + self.e["providers"][0].token])
        self.assertNotIn("Bearer " + self.token, seen)

    def test_budget_reservation_prevents_call(self):
        self.engine.policy["tenants"]["government"]["budget_credits"] = 1
        self.denied("budget_exhausted", self.generate)
        self.assertEqual(self.e["providers"][0].calls, 0)

    def test_failed_attempt_is_still_charged(self):
        self.e["providers"][0].mode = "unavailable"
        self.generate()
        self.assertEqual(self.store.spent("government"),
                         (len(REQUEST["prompt"].encode()) + 256) * 5)

    def test_rate_limit_persists_per_tenant(self):
        self.engine.policy["tenants"]["government"]["requests_per_minute"] = 1
        self.generate()
        self.denied("rate_exceeded", lambda: self.generate(key="request-2"))
        self.assertEqual(self.generate(key="bank-request", token=self.e["tokens"]["bfsi"])["model"], "local-standard")

    def test_idempotency_replay_does_not_call_provider_twice(self):
        first = self.generate()
        self.assertEqual(self.generate(), first)
        self.assertEqual(self.e["providers"][0].calls, 1)

    def test_idempotency_key_cannot_change_payload(self):
        self.generate()
        self.denied("idempotency_conflict", lambda: self.generate({**REQUEST, "prompt": "Changed"}))

    def test_idempotency_cache_is_tenant_scoped(self):
        self.generate()
        self.generate(token=self.e["tokens"]["bfsi"])
        self.assertEqual(self.e["providers"][0].calls, 2)

    def test_idempotency_cache_is_subject_scoped(self):
        self.generate()
        second = Principal("second-gov-app", "government", ("knowledge-assistant",), ("generate",))
        self.generate(token=self.e["identity"].issue(second))
        self.assertEqual(self.e["providers"][0].calls, 2)

    def test_retrieval_acl_checked_before_cached_replay(self):
        req = {**REQUEST, "document_id": "gov-doc"}
        self.generate(req)
        self.engine.documents["gov-doc"]["subjects"] = []
        self.denied("document_access_denied", lambda: self.generate(req))

    def test_cached_response_model_review_is_rechecked(self):
        self.generate()
        self.engine.policy["models"]["local-standard"]["review_expires"] = self.clock.now
        self.denied("cached_route_no_longer_eligible", self.generate)
        self.assertEqual(self.e["providers"][0].calls, 1)

    def test_concurrent_idempotency_executes_once(self):
        self.e["providers"][0].mode = "timeout"
        def run(_):
            try:
                return self.generate()
            except Denied as error:
                return error.code
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(run, range(8)))
        self.assertEqual(self.e["providers"][0].calls, 1)
        self.assertTrue(all(isinstance(r, dict) or r == "request_in_progress" for r in results))

    def test_concurrent_budget_reservation_is_atomic(self):
        credits = (len(REQUEST["prompt"].encode()) + 256) * 2
        self.engine.policy["tenants"]["government"]["budget_credits"] = credits
        def run(i):
            try:
                return self.generate(key=f"parallel-{i}")
            except Denied as error:
                return error.code
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(run, range(8)))
        self.assertEqual(sum(isinstance(r, dict) for r in results), 1)
        self.assertEqual(self.store.spent("government"), credits)

    def test_open_circuit_skips_failing_model(self):
        self.e["providers"][0].mode = "unavailable"
        self.generate(key="circuit-1")
        self.generate(key="circuit-2")
        self.generate(key="circuit-3")
        self.assertEqual(self.e["providers"][0].calls, 2)
        self.clock.now += 6
        self.e["providers"][0].mode = "ok"
        self.assertEqual(self.generate(key="circuit-4")["model"], "local-standard")

    def test_model_proposal_does_not_execute_a_tool(self):
        self.e["providers"][0].mode = "propose-tool"
        self.generate({**REQUEST, "document_id": "injection-doc"})
        self.assertEqual(self.store.db.execute("SELECT COUNT(*) FROM actions").fetchone()[0], 0)

    def test_tool_requires_two_approvals(self):
        self.denied("two_approvals_required", lambda: self.invoke(copy.deepcopy(ACTION)))

    def test_two_independent_approvals_execute_synthetic_action(self):
        result = self.invoke({**ACTION, "approvals": self.approvals()})
        self.assertEqual(result["status"], "synthetic_action_recorded")
        self.assertTrue(self.store.audit_valid())

    def test_approval_replay_denied(self):
        value = {**ACTION, "approvals": self.approvals()}
        self.invoke(value)
        self.denied("invalid_action_approval", lambda: self.invoke(value))

    def test_changed_arguments_invalidate_approvals(self):
        value = {**ACTION, "arguments": {"asset": "asset-a", "window": "night"},
                 "approvals": self.approvals()}
        self.denied("invalid_action_approval", lambda: self.invoke(value))

    def test_expired_approvals_denied(self):
        value = {**ACTION, "approvals": self.approvals()}
        self.clock.now += 121
        self.denied("invalid_action_approval", lambda: self.invoke(value))

    def test_same_reviewer_twice_denied(self):
        value = {"requester": "gov-app", "action": ACTION}
        token = self.e["tokens"]["reviewer-a"]
        handles = [self.engine.dispatch(token, "/v1/approvals", value)["approval"] for _ in range(2)]
        self.denied("distinct_reviewers_required", lambda: self.invoke({**ACTION, "approvals": handles}))

    def test_workload_cannot_approve(self):
        self.denied("scope_denied", lambda: self.engine.dispatch(
            self.token, "/v1/approvals", {"requester": "gov-app", "action": ACTION}))

    def test_self_approval_denied(self):
        self.denied("independent_reviewer_required", lambda: self.engine.dispatch(
            self.e["tokens"]["reviewer-a"], "/v1/approvals", {"requester": "reviewer-a", "action": ACTION}))

    def test_cross_tenant_tool_target_denied(self):
        self.denied("asset_access_denied", lambda: self.invoke(
            {**ACTION, "arguments": {"asset": "asset-b", "window": "day"}}))

    def test_unknown_tool_denied(self):
        self.denied("tool_not_allowed", lambda: self.invoke({**ACTION, "tool": "shell.execute"}))

    def test_malformed_approval_action_is_client_error(self):
        self.denied("invalid_fields", lambda: self.engine.dispatch(
            self.e["tokens"]["reviewer-a"], "/v1/approvals", {"requester": "gov-app", "action": []}))

    def test_output_limit_is_enforced(self):
        self.denied("output_limit_exceeded", lambda: self.generate({**REQUEST, "max_output_bytes": 1025}))

    def test_boolean_is_not_accepted_as_integer(self):
        self.denied("invalid_integer", lambda: self.generate({**REQUEST, "max_output_bytes": True}))

    def test_duplicate_json_key_rejected_on_wire(self):
        status, result = self.http(b'{"use_case":"unknown","use_case":"knowledge-assistant"}')
        self.assertEqual((status, result["error"]), (400, "duplicate_json_key"))

    def test_nonfinite_json_rejected(self):
        status, result = self.http(b'{"number":NaN}')
        self.assertEqual((status, result["error"]), (400, "invalid_json"))

    def test_wrong_media_type_rejected(self):
        status, result = self.http(canonical(REQUEST), {"Content-Type": "text/plain"})
        self.assertEqual((status, result["error"]), (415, "unsupported_media_type"))

    def test_large_body_rejected_before_parse(self):
        status, result = self.http(b"x" * 32769)
        self.assertEqual((status, result["error"]), (413, "invalid_body_size"))

    def test_audit_has_no_prompt_response_or_bearer(self):
        self.generate()
        text = json.dumps(self.store.audit_rows())
        self.assertNotIn(REQUEST["prompt"], text)
        self.assertNotIn("Synthetic answer", text)
        self.assertNotIn(self.token, text)

    def test_encrypted_idempotency_response_is_not_plaintext(self):
        self.generate()
        text = self.store.db.execute("SELECT response FROM requests").fetchone()[0]
        self.assertNotIn("Synthetic answer", text)
        self.assertTrue(all(c in "0123456789abcdef" for c in text))

    def test_audit_alteration_detected(self):
        self.generate()
        self.store.db.execute("UPDATE audit SET event='{}' WHERE id=1")
        self.assertFalse(self.store.audit_valid())

    def test_audit_suffix_deletion_is_known_gap_without_external_anchor(self):
        self.generate()
        self.store.db.execute("DELETE FROM audit WHERE id=(SELECT MAX(id) FROM audit)")
        self.assertTrue(self.store.audit_valid())

    def test_html_output_is_json_data_not_executed(self):
        self.e["providers"][0].mode = "html"
        status, result = self.http(canonical(REQUEST))
        self.assertEqual(status, 200)
        self.assertIn("<script>", result["text"])

    def test_obfuscated_email_is_known_gap_in_fixture_detector(self):
        result = self.generate({**REQUEST, "prompt": "person [at] example [dot] com"})
        self.assertEqual(result["model"], "local-standard")

    def test_credential_revoked_during_provider_call_blocks_response(self):
        adapter = self.engine.adapters["provider-a"]
        original = adapter.generate
        def revoke_then_return(*args):
            response = original(*args)
            self.e["identity"].revoke(self.token)
            return response
        adapter.generate = revoke_then_return
        self.denied("invalid_credential", self.generate)

    def test_response_key_loss_fails_closed(self):
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        self.generate()
        self.store.cipher = AESGCM(AESGCM.generate_key(bit_length=256))
        self.denied("cached_response_key_unavailable", self.generate)
        self.assertEqual(self.e["providers"][0].calls, 1)

    def test_tool_action_and_completion_audit_share_one_transaction(self):
        approvals = self.approvals()
        self.store.db.execute("CREATE TRIGGER prevent_action_audit BEFORE INSERT ON audit "
                             "WHEN NEW.event LIKE '%synthetic_tool_completed%' "
                             "BEGIN SELECT RAISE(ABORT,'injected audit failure'); END;")
        import sqlite3
        with self.assertRaises(sqlite3.IntegrityError):
            self.invoke({**ACTION, "approvals": approvals})
        self.assertEqual(self.store.db.execute("SELECT COUNT(*) FROM actions").fetchone()[0], 0)
        self.store.db.execute("DROP TRIGGER prevent_action_audit")
        self.assertEqual(self.invoke({**ACTION, "approvals": approvals})["status"], "synthetic_action_recorded")


class AdmissionAndStateCases(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.key = Ed25519PrivateKey.generate()
        self.trust = {"governance": self.key.public_key().public_bytes_raw()}
        self.policy = sample_policy(self.clock.now)
        self.envelope = sign_policy(self.policy, "governance", self.key)
    def admit(self, envelope=None, minimum=1):
        return admit_policy(envelope or self.envelope, self.trust, "lab-site-a", minimum, self.clock())
    def denied(self, code, call):
        with self.assertRaises(Denied) as caught:
            call()
        self.assertEqual(caught.exception.code, code)

    def test_valid_signed_policy_admitted(self):
        self.assertEqual(self.admit().sha256, digest(self.policy))

    def test_altered_signed_policy_denied(self):
        self.envelope["policy"]["revision"] = 2
        self.denied("invalid_policy_signature", self.admit)

    def test_unexpected_signer_denied(self):
        self.envelope["signer_id"] = "attacker"
        self.denied("untrusted_policy_signer", self.admit)

    def test_signature_under_wrong_key_denied(self):
        wrong = Ed25519PrivateKey.generate()
        self.denied("invalid_policy_signature", lambda: self.admit(sign_policy(self.policy, "governance", wrong)))

    def test_policy_for_other_site_denied(self):
        self.policy["site"] = "other-site"
        self.denied("wrong_policy_site", lambda: self.admit(sign_policy(self.policy, "governance", self.key)))

    def test_old_revision_denied(self):
        self.denied("policy_rollback", lambda: self.admit(minimum=2))

    def test_expired_signed_policy_denied(self):
        self.clock.now += 3600
        self.denied("policy_not_current", self.admit)

    def test_future_policy_denied(self):
        self.clock.now -= 10
        self.denied("policy_not_current", self.admit)

    def test_model_missing_owner_denied(self):
        del self.policy["models"]["local-standard"]["owner"]
        self.denied("invalid_fields", lambda: self.admit(sign_policy(self.policy, "governance", self.key)))

    def test_unknown_model_reference_denied(self):
        self.policy["use_cases"]["knowledge-assistant"]["models"] = ["unregistered"]
        self.denied("invalid_model_reference", lambda: self.admit(sign_policy(self.policy, "governance", self.key)))

    def test_arbitrary_network_endpoint_denied(self):
        for url in ("http://169.254.169.254/infer", "https://evil.test/infer", "http://localhost:80/infer",
                    "http://127.0.0.1:80/infer?redirect=x", "http://user:pass@127.0.0.1:80/infer"):
            with self.subTest(url=url):
                self.denied("invalid_provider_endpoint", lambda: LoopbackAdapter(url, "fixture"))

    def test_durable_budget_and_rollback_watermark_survive_reopen(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / "state.sqlite")
            store = Store(path, self.clock)
            store.reserve("government", 100, 100, 10)
            store.accept_revision("lab-site-a", 2)
            store.close()
            reopened = Store(path, self.clock)
            try:
                self.assertEqual(reopened.spent("government"), 100)
                self.denied("budget_exhausted", lambda: reopened.reserve("government", 1, 100, 10))
                self.denied("policy_rollback", lambda: reopened.accept_revision("lab-site-a", 1))
            finally:
                reopened.close()

    def test_backup_restore_requires_separate_response_key(self):
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        key = AESGCM.generate_key(bit_length=256)
        with tempfile.TemporaryDirectory() as directory:
            source = Store(str(Path(directory) / "source.sqlite"), self.clock, key)
            source.claim("request", "fingerprint")
            source.finish("request", {"text": "Synthetic secret response"})
            source.reserve("government", 50, 100, 10)
            backup = str(Path(directory) / "backup.sqlite")
            source.backup(backup)
            source.close()
            wrong = Store(backup, self.clock)
            self.denied("cached_response_key_unavailable", lambda: wrong.claim("request", "fingerprint"))
            wrong.close()
            correct = Store(backup, self.clock, key)
            try:
                self.assertEqual(correct.claim("request", "fingerprint")["text"], "Synthetic secret response")
                self.assertEqual(correct.spent("government"), 50)
            finally:
                correct.close()

    def test_running_request_does_not_reexecute_after_lease_expiry(self):
        store = Store(":memory:", self.clock)
        try:
            store.claim("request", "fingerprint")
            self.clock.now += 31
            self.denied("request_in_progress", lambda: store.claim("request", "fingerprint"))
        finally:
            store.close()

    def test_same_policy_revision_cannot_change_digest(self):
        store = Store(":memory:", self.clock)
        try:
            store.accept_revision("lab-site-a", 1, "a" * 64)
            self.denied("policy_revision_conflict",
                        lambda: store.accept_revision("lab-site-a", 1, "b" * 64))
        finally:
            store.close()

    def test_reference_server_cannot_bind_public_interface(self):
        with self.assertRaises(ValueError):
            BoundedServer(("0.0.0.0", 0), gateway_handler(None))


if __name__ == "__main__":
    unittest.main()
