# Failure behavior and availability

**Implemented:** real loopback HTTP adapters have a bounded timeout and response size. Redirects are not followed. A transport availability failure may select one further eligible model; malformed or sensitive output does not trigger a fallback that bypasses a validation failure. Two consecutive availability failures open a five-second local circuit.

Every attempt reserves worst-case synthetic byte credits before provider I/O. Failed/ambiguous attempts remain charged. Attempt limits are per tenant/minute; they do not replace ingress abuse controls.

Idempotency includes tenant, subject, request and policy/document context. A running record stays blocked after expiry; operator recovery is needed after a crash. This favors avoiding duplicate execution over automatic availability. Tools use single-use approvals rather than retrying side effects.

**Target:** define an end-to-end timeout budget, retry ownership, cancellation, streaming termination, durable leases, dependency health, state failure modes, backup/key recovery, HA quorum and disaster recovery. If no eligible endpoint remains, fail closed.

Provider success is not task success. The fixture cannot establish real-model availability, factuality or customer experience. [Benchmark scope](benchmarks.md) and [production gates](production-readiness.md) explain the limits.
