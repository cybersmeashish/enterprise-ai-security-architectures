# 11 — SSE, multi-agent traces, incident debugging and prompt rollback

## SSE and disconnects

For browser chat, use an authenticated request to create a run followed by an authorised stream, or an approved fetch-based SSE transport. Native EventSource header limitations affect token transport; never put a durable secret in a query URL. Bind run ID to the current subject/case. SSE events contain sequence ID, event type and one JSON data object; use heartbeat comments, no-store headers and proxy-buffering controls.

Record `received`, `retrieval_complete`, `needs_review`, `answer` and `done` separately. A retrieval-progress event is not the first safe answer token. Verify citations and disclosure before visible answer material. For high-risk legal material, buffer the answer for validation; low-risk progressive display needs an explicit reviewed safety boundary.

On disconnect cancel generation/tool work where possible and release KV/worker resources. If background continuation is approved, cap its budget and retention. A reconnect uses a cursor and an authorised, short-lived replay buffer; `Last-Event-ID` is not authentication. Recheck grants on reconnect. If evidence/policy changed or the cursor expired, return an explicit restart state rather than silently replaying stale sensitive text. Use idempotent run creation and outcome lookup so reconnection cannot duplicate an action.

## Trace every step of a multi-agent workflow

Prefer one bounded orchestrator until multiple agents demonstrably add value. If decomposed, assign distinct contracts: retrieval, evidence checking and drafting. No agent may grant another new authority or self-approve a sensitive action. Propagate verified scope and a root task budget; parallel agents must share aggregate limits.

Create a root trace with child spans for authentication/policy, redaction, cache, sparse/dense search, merge/rerank, parent expansion, prompt assembly, model attempts, tool calls, approvals, validation and stream lifecycle. Link asynchronous ingest/case events and distributed child tasks with trace/span relationships. Record model/prompt/schema versions, index/corpus/grant epochs, candidate IDs/ranks, token use, queue wait, retry count, cancellation and outcome class. Protected payload capture is off by default.

Record who observed or changed what, where and when; include clock uncertainty for regional/offline stages. Prevent model-written trace fields from masquerading as verified identity. Apply trace ACLs, redaction, tamper controls and retention. OpenTelemetry's GenAI conventions are an implementation reference with stability/version checks, not a guarantee that a framework automatically traces the workflow correctly.

## Roll back a bad prompt change

Prompts are versioned artifacts coupled to model, schema, tool contract, retrieval settings and safety policy. Use immutable signed release manifests and one deployment alias. Before promotion run boundary tests, sealed paired evaluations and a shadow/canary cohort with human review for material cases. Declare automatic stop conditions for disclosure, material error, refusal, latency and spend.

When a canary regresses, freeze expansion and switch the alias to the known-good compatible release. Invalidate affected answer/prefix caches, stop or explicitly finish old runs, and revalidate memory summaries as needed. Do not roll back to an index/policy version that resurrects revoked grants. Audit the operator, incident reason, time, affected runs and restored version. Verify the known-good smoke suite and watch the same metrics through recovery.

A prompt rollback cannot undo a disclosure or external side effect. Trigger incident handling and downstream remediation separately. The lab tests a version-bound cache and schema/agent boundaries; it does not deploy or roll back a production prompt.
