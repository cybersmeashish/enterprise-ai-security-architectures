"""Deterministic authorization precedes routing, retrieval and synthetic tool actions."""
import copy
import re
import threading
from .contracts import (CLASSES, Denied, canonical, digest, fields, generate_request,
                        identifier, tool_action)
from .policy import VerifiedPolicy

# Deliberately narrow fixtures. These are NOT general PII or prompt-injection detectors.
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
SECRET = re.compile(r"\bDEMO_SECRET_[A-Za-z0-9]+\b")


class Engine:
    def __init__(self, verified, identity, store, adapters, documents, assets, clock):
        if not isinstance(verified, VerifiedPolicy):
            raise Denied("verified_policy_required")
        self.policy = copy.deepcopy(verified.value)
        self.policy_hash = verified.sha256
        self.identity, self.store, self.adapters = identity, store, adapters
        self.documents, self.assets, self.clock = copy.deepcopy(documents), copy.deepcopy(assets), clock
        self.circuits, self.circuit_lock = {}, threading.RLock()
        store.accept_revision(self.policy["site"], self.policy["revision"], self.policy_hash)

    def context(self, token, scope, case_id):
        principal = self.identity.resolve(token)
        if not self.policy["issued_at"] <= self.clock() < self.policy["expires_at"]:
            raise Denied("policy_not_current")
        if principal.tenant not in self.policy["tenants"] or scope not in principal.scopes:
            raise Denied("scope_denied")
        case = self.policy["use_cases"].get(case_id)
        if case_id not in principal.use_cases or not case:
            raise Denied("use_case_denied")
        if case["state"] != "approved" or self.clock() >= case["review_expires"]:
            raise Denied("use_case_not_current")
        return principal, case

    def dispatch(self, token, path, value, idempotency=None):
        principal = None
        try:
            principal = self.identity.resolve(token)
            if path == "/v1/generate":
                return self.generate(token, value, idempotency)
            if path == "/v1/approvals":
                return self.approve(token, value)
            if path == "/v1/tools/invoke":
                return self.invoke(token, value)
            raise Denied("unknown_endpoint", 404)
        except Denied as error:
            self.store.audit({"time": int(self.clock()), "event": "denied", "code": error.code,
                              "subject": principal.subject if principal else None,
                              "tenant": principal.tenant if principal else None,
                              "policy": self.policy_hash})
            raise

    def generate(self, token, value, idempotency):
        generate_request(value)
        identifier(idempotency)
        principal, case = self.context(token, "generate", value["use_case"])
        if value["max_output_bytes"] > case["max_output_bytes"]:
            raise Denied("output_limit_exceeded", 400)
        level = max(CLASSES.index(case["minimum_classification"]),
                    CLASSES.index(value.get("classification", "public")))
        prompt = value["prompt"]
        document_digest = None
        if "document_id" in value:
            doc = self.documents.get(value["document_id"])
            if (not doc or doc["tenant"] != principal.tenant
                    or principal.subject not in doc["subjects"]):
                raise Denied("document_access_denied")
            level = max(level, CLASSES.index(doc["classification"]))
            document_digest = digest(doc)
            prompt += "\n[UNTRUSTED_RETRIEVED_CONTEXT]\n" + doc["text"]
        if len(prompt.encode()) > 16384:
            raise Denied("combined_input_too_large", 400)
        if EMAIL.search(prompt) or SECRET.search(prompt):
            raise Denied("fixture_sensitive_input")
        candidates = self.eligible(case, CLASSES[level])
        if not candidates:
            raise Denied("no_eligible_model", 503)
        key = digest({"tenant": principal.tenant, "subject": principal.subject, "key": idempotency})
        fingerprint = digest({"request": value, "policy": self.policy_hash, "document": document_digest})
        cached = self.store.claim(key, fingerprint)
        if cached:
            # All live authorization, retrieval and eligibility checks occur before replay.
            if "error" in cached:
                raise Denied(cached["error"], cached["status"])
            if cached["model"] not in candidates:
                raise Denied("cached_route_no_longer_eligible")
            return cached
        try:
            result = self.execute_models(token, principal, case, value, prompt, candidates)
            self.store.finish(key, result)
            return result
        except Denied as error:
            self.store.finish(key, {"error": error.code, "status": error.status})
            raise

    def eligible(self, case, classification):
        now = self.clock()
        candidates = []
        for model_id in case["models"]:
            model = self.policy["models"][model_id]
            with self.circuit_lock:
                _, until = self.circuits.get(model_id, (0, 0))
            if (model["state"] == "approved" and now < model["review_expires"]
                    and classification in model["classes"] and model["region"] in case["regions"]
                    and model["endpoint_ref"] in self.adapters and now >= until):
                candidates.append((model["credit_per_byte"], model_id))
        return [item[1] for item in sorted(candidates)]

    def execute_models(self, token, principal, case, value, prompt, candidates):
        tenant = self.policy["tenants"][principal.tenant]
        last = Denied("provider_unavailable", 503)
        for attempt, model_id in enumerate(candidates[:2], 1):
            # Recheck review, identity and eligibility before each external attempt.
            self.context(token, "generate", value["use_case"])
            level = max(CLASSES.index(case["minimum_classification"]),
                        CLASSES.index(value.get("classification", "public")))
            if "document_id" in value:
                level = max(level, CLASSES.index(self.documents[value["document_id"]]["classification"]))
            if model_id not in self.eligible(case, CLASSES[level]):
                continue
            model = self.policy["models"][model_id]
            credits = (len(prompt.encode()) + value["max_output_bytes"]) * model["credit_per_byte"]
            self.store.reserve(principal.tenant, credits, tenant["budget_credits"], tenant["requests_per_minute"])
            event = {"time": int(self.clock()), "subject": principal.subject, "tenant": principal.tenant,
                     "use_case": value["use_case"], "model": model_id, "region": model["region"],
                     "policy": self.policy_hash, "attempt": attempt, "reserved_demo_credits": credits}
            self.store.audit({**event, "event": "provider_attempt"})
            try:
                text = self.adapters[model["endpoint_ref"]].generate(
                    prompt, value["max_output_bytes"], model_id)
            except Denied as error:
                last = error
                with self.circuit_lock:
                    failures, _ = self.circuits.get(model_id, (0, 0))
                    failures += 1
                    self.circuits[model_id] = (failures, self.clock() + 5 if failures >= 2 else 0)
                self.store.audit({**event, "event": "provider_failure", "code": error.code})
                # Only transport availability failures permit an eligible fallback.
                if error.code != "provider_unavailable":
                    raise
                continue
            self.context(token, "generate", value["use_case"])
            if model_id not in self.eligible(case, CLASSES[level]):
                raise Denied("route_no_longer_eligible")
            if EMAIL.search(text) or SECRET.search(text):
                raise Denied("fixture_sensitive_output", 502)
            with self.circuit_lock:
                self.circuits[model_id] = (0, 0)
            self.store.audit({**event, "event": "completed", "output_bytes": len(text.encode())})
            return {"text": text, "model": model_id, "region": model["region"],
                    "policy_revision": self.policy["revision"], "policy_sha256": self.policy_hash,
                    "attempts": attempt, "metering": "synthetic_byte_credits"}
        raise last

    def authorized_action(self, token, value, scope):
        tool_action(value)
        principal, case = self.context(token, scope, value["use_case"])
        if value["tool"] not in case["tools"]:
            raise Denied("tool_not_allowed")
        asset = self.assets.get(value["arguments"]["asset"])
        if not asset or asset["tenant"] != principal.tenant:
            raise Denied("asset_access_denied")
        action = digest({"requester": principal.subject, "tenant": principal.tenant,
                         "use_case": value["use_case"], "tool": value["tool"],
                         "arguments": value["arguments"], "policy": self.policy_hash})
        return principal, action

    def approve(self, token, value):
        fields(value, ("requester", "action"))
        identifier(value["requester"])
        tool_action(value["action"])
        principal, case = self.context(token, "approve", value["action"]["use_case"])
        if principal.role != "reviewer" or value["requester"] == principal.subject:
            raise Denied("independent_reviewer_required")
        if value["action"]["tool"] not in case["tools"] or value["action"].get("approvals"):
            raise Denied("invalid_approval_action", 400)
        asset = self.assets.get(value["action"]["arguments"]["asset"])
        if not asset or asset["tenant"] != principal.tenant:
            raise Denied("asset_access_denied")
        action = digest({"requester": value["requester"], "tenant": principal.tenant,
                         "use_case": value["action"]["use_case"], "tool": value["action"]["tool"],
                         "arguments": value["action"]["arguments"], "policy": self.policy_hash})
        self.store.audit({"time": int(self.clock()), "event": "approval_issued",
                          "tenant": principal.tenant, "reviewer": principal.subject,
                          "action_digest": action, "policy": self.policy_hash})
        handle = self.store.approve(principal, value["requester"], action)
        return {"approval": handle, "action_digest": action, "expires_in_seconds": 120}

    def invoke(self, token, value):
        principal, action = self.authorized_action(token, value, "invoke")
        self.store.audit({"time": int(self.clock()), "event": "tool_attempt",
                          "tenant": principal.tenant, "subject": principal.subject,
                          "action_digest": action, "policy": self.policy_hash})
        action_id = self.store.execute_action(principal, action, value.get("approvals", []))
        return {"status": "synthetic_action_recorded", "action_id": action_id, "action_digest": action}
