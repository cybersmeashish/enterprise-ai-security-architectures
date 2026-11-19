"""Measured HTTP fixture experiments, including explicit failed assurance hypotheses."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import errno
import http.client
import json
import os
from pathlib import Path
import platform
import socket
import tempfile
import time
from aiegateway.contracts import Denied, canonical
from aiegateway.fixtures import environment

REQUEST = {"use_case": "knowledge-assistant", "prompt": "Summarize the synthetic approved procedure.",
           "max_output_bytes": 256}
ACTION = {"use_case": "site-maintenance", "tool": "maintenance.schedule",
          "arguments": {"asset": "asset-a", "window": "day"}}


def http_call(env, request, key, tenant="government"):
    conn = http.client.HTTPConnection("127.0.0.1", env["server"].server_port, timeout=3)
    start = time.perf_counter()
    try:
        conn.request("POST", "/v1/generate", canonical(request),
                     {"Content-Type": "application/json", "Authorization": "Bearer " + env["tokens"][tenant],
                      "Idempotency-Key": key})
        response = conn.getresponse()
        body = json.loads(response.read())
        return {"status": response.status, "body": body,
                "milliseconds": (time.perf_counter() - start) * 1000}
    finally:
        conn.close()


def isolation():
    interfaces = sorted(p.name for p in Path("/sys/class/net").iterdir()) if Path("/sys/class/net").exists() else []
    probe = socket.socket()
    probe.settimeout(0.1)
    try:
        result = probe.connect_ex(("1.1.1.1", 443))
    finally:
        probe.close()
    return {"interfaces": interfaces, "external_probe_errno": result,
            "external_probe_unreachable": result in (errno.ENETUNREACH, errno.EHOSTUNREACH),
            "uid": os.getuid(), "only_loopback": interfaces == ["lo"]}


def percentile(values, probability):
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    low = int(position)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def run_experiment(samples=60):
    results, benchmarks = [], []
    with tempfile.TemporaryDirectory() as directory:
        with environment(str(Path(directory) / "gateway.sqlite"), start_http=True) as env:
            def case(name, request, key, expected_status, expected_code=None, tenant="government"):
                value = http_call(env, request, key, tenant)
                passed = value["status"] == expected_status
                if expected_code:
                    passed = passed and value["body"].get("error") == expected_code
                results.append({"id": name, "passed": passed, **value})
                if not passed:
                    raise AssertionError(name)
                return value
            first = case("allowed-local-route", REQUEST, "case-1", 200)
            assert first["body"]["model"] == "local-standard"
            before = env["providers"][0].calls
            replay = case("same-principal-idempotency-replay", REQUEST, "case-1", 200)
            assert replay["body"] == first["body"] and env["providers"][0].calls == before
            case("tenant-spoof-denied", {**REQUEST, "tenant": "bfsi"}, "case-2", 400, "invalid_fields")
            case("cross-tenant-retrieval-denied", {**REQUEST, "document_id": "bank-doc"}, "case-3",
                 403, "document_access_denied")
            case("retrieval-authorized", {**REQUEST, "document_id": "gov-doc"}, "case-4", 200)
            case("fixture-secret-denied", {**REQUEST, "prompt": "DEMO_SECRET_TEST"}, "case-5",
                 403, "fixture_sensitive_input")
            case("separate-bank-tenant", REQUEST, "case-1", 200, tenant="bfsi")
            env["providers"][0].mode = "unavailable"
            fallback = case("approved-local-fallback", REQUEST, "case-6", 200)
            assert fallback["body"]["model"] == "local-backup"
            env["providers"][0].mode = "ok"
            env["providers"][0].mode = "propose-tool"
            case("indirect-injection-cannot-authorize-tool",
                 {**REQUEST, "document_id": "injection-doc"}, "case-7", 200)
            assert env["store"].db.execute("SELECT COUNT(*) FROM actions").fetchone()[0] == 0
            env["providers"][0].mode = "ok"
            engine, token = env["engine"], env["tokens"]["government"]
            approvals = [engine.dispatch(env["tokens"][reviewer], "/v1/approvals",
                         {"requester": "gov-app", "action": ACTION})["approval"]
                         for reviewer in ("reviewer-a", "reviewer-b")]
            action = {**ACTION, "approvals": approvals}
            executed = engine.dispatch(token, "/v1/tools/invoke", action)
            results.append({"id": "two-reviewer-synthetic-action", "passed": True,
                            "status": 200, "body": executed})
            try:
                engine.dispatch(token, "/v1/tools/invoke", action)
                raise AssertionError("Approval replay unexpectedly accepted")
            except Denied as error:
                assert error.code == "invalid_action_approval"
                results.append({"id": "approval-replay-denied", "passed": True,
                                "status": error.status, "body": {"error": error.code}})
            assert env["store"].audit_valid()
            results.append({"id": "local-audit-chain-valid", "passed": True, "status": 200})
            # Warm-up is excluded; every timed request uses a unique idempotency key.
            for i in range(5):
                assert http_call(env, REQUEST, f"warmup-{i}")["status"] == 200
            for concurrency in (1, 4, 8):
                start = time.perf_counter()
                with ThreadPoolExecutor(max_workers=concurrency) as pool:
                    batch = list(pool.map(lambda i: http_call(env, REQUEST, f"bench-{concurrency}-{i}"),
                                          range(samples)))
                seconds = time.perf_counter() - start
                times = [item["milliseconds"] for item in batch]
                successes = sum(item["status"] == 200 for item in batch)
                assert successes == samples
                benchmarks.append({"concurrency": concurrency, "requests": samples,
                                   "successes": successes, "errors": samples - successes,
                                   "seconds": seconds, "successful_requests_per_second": successes / seconds,
                                   "latency_ms": {"min": min(times), "p50": percentile(times, .5),
                                                  "p95": percentile(times, .95), "p99": percentile(times, .99),
                                                  "max": max(times)}})
            spent_before = env["store"].spent("government")
            backup = str(Path(directory) / "restored.sqlite")
            started = time.perf_counter()
            env["store"].backup(backup)
            from aiegateway.store import Store
            restored = Store(backup, time.time)
            try:
                assert restored.spent("government") == spent_before and restored.audit_valid()
                restore_seconds = time.perf_counter() - started
                restoration = {"passed": True, "snapshot_spend_credits": spent_before,
                               "restored_spend_credits": restored.spent("government"),
                               "backup_and_open_seconds": restore_seconds,
                               "scope": "local SQLite consistent snapshot, budget and audit verification",
                               "response_replay": "requires separately retained AES-GCM key",
                               "missing_external_dependencies": ["identity issuer", "provider inventory authority",
                                                                 "external audit checkpoint", "production KMS"]}
            finally:
                restored.close()
            audit_count = len(env["store"].audit_rows())
            assert env["providers"][2].calls == 0
    return {"experiment": "enterprise-ai-gateway-synthetic-http-v1",
            "run_at": datetime.now(timezone.utc).isoformat(),
            "environment": {"python": platform.python_version(), "platform": platform.platform(),
                            "machine": platform.machine(), "logical_cpus": os.cpu_count(),
                            "model": "deterministic loopback fixture; no learned model",
                            "storage": "SQLite in a temporary filesystem directory",
                            "transport": "new loopback HTTP connection per request",
                            "warmup_requests": 5, "sample_count_per_cohort": samples},
            "scenarios": results, "benchmarks": benchmarks, "restoration": restoration,
            "audit_events": audit_count,
            "known_gaps": [
                {"id": "obfuscated-pii", "evidence": "test_obfuscated_email_is_known_gap_in_fixture_detector",
                 "result": "obfuscated email is accepted; regex is not a DLP product"},
                {"id": "audit-truncation", "evidence": "test_audit_suffix_deletion_is_known_gap_without_external_anchor",
                 "result": "suffix deletion passes local chain verification without an external checkpoint"},
                {"id": "html-consumer", "evidence": "test_html_output_is_json_data_not_executed",
                 "result": "HTML remains untrusted JSON data; the consuming app must sanitize before rendering"},
                {"id": "large-scale", "result": "HA, distributed quotas and real inference throughput are unmeasured"}],
            "limitations": ["Synthetic byte credits are not provider billing or tokenizer counts.",
                            "Microbenchmarks include fixture provider and SQLite overhead.",
                            "No task-quality, fairness, factuality, production SLA or enterprise-capacity claim."]}
