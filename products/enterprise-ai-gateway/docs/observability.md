# Security evidence and operational visibility

**Implemented:** local audit fields record trusted subject/tenant, event, policy hash, use case, model, declared region, attempt, reserved demo credits and output size. Prompt, output text, bearer credentials and approval handles are excluded. Ordinary record alteration is detected by a hash chain.

**Observed limitation:** deleting the last record leaves a locally valid chain. A privileged party can also rewrite records and recompute it. Establish completeness with externally anchored checkpoints, independent storage/custody, expected-event reconciliation and explicit time uncertainty.

The product uses its own metadata schema. It does **not** export OpenTelemetry or claim GenAI semantic-convention conformance. The primary OpenTelemetry documentation reviewed on 19 November 2026 indicates that GenAI conventions moved to a dedicated repository; validate the maintained version before instrumenting.

| Proposed indicator | Decision | Owner |
|---|---|---|
| Eligible-route failures by use case | Disable unsafe fallback; assess capacity | SRE |
| Denials by stable reason, without content | Investigate compromised identity or policy drift | Security operations |
| Policy/review age and current revision | Refresh/retire authority | AI governance |
| Ambiguous attempts and reserved-vs-billed cost | Reconcile spend | FinOps |
| Evidence freshness, missing sequences, clock confidence | Limit central conclusions | Evidence owner |

Metadata is still governed data. Access, retention, deletion, export recipient, support access and incident custody need production implementation.
