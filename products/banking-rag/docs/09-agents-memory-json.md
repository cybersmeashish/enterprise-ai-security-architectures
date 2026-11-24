# 09 — Reliable tools, loop repair, long-running memory and valid JSON

## Tool reliability

Start with a read-only agent. Tools are registered, narrow operations such as `lookup_authorised_receipt`, `fetch_clause_version` and `open_review_ticket`. Avoid arbitrary SQL, shell, browser access and recipient-selected exports. Server-side context binds identity/case/purpose; the model supplies only allowed arguments. Validate schemas, independently authorise the operation, enforce deadlines, bounded output and idempotency, and record attempts/outcomes. Tool output is evidence, not executable instruction.

Classify failures: transient timeouts may receive bounded jittered retries; permission/schema/resource-not-found failures do not. A timed-out write may have completed, so retry only with the same idempotency key or query status. Financial or material actions remain outside the first release and require separate human approval bound to exact action fields.

## Fix a looping agent

Keep explicit state: goal, permitted operations, completed effects, unresolved evidence, cumulative tokens/cost/time and tool call history. Hash canonical arguments together with tool and relevant state version. A repeated call with unchanged state is a loop signal; a legitimately changed state is not. Enforce maximum steps (eight as an initial reference), per-tool retries, wall-clock deadline and cumulative budget.

On no progress, stop rather than invent a result. Return `needs_review` with a concise summary, the failed operation and known evidence. Use one controlled replan only if it can acquire new authorised evidence within remaining budget. Cancellation reaches workers and in-flight calls. Alert on loop rate and task-level spend. The lab demonstrates repeated-call detection and step ceilings without a learned agent or real bank tools.

## Memory for a long-running assistant

Separate request context, conversation state, task state and durable memory. Request context contains current grants and cannot be inherited from a previous chat. Summaries are untrusted interpretations; never turn a retrieved instruction or a user's claim into a durable policy. Durable facts require an authoritative source, owner, provenance, version, expiry and permitted purpose.

Use encrypted, per-subject/case stores; store references instead of raw PII where possible. Reauthorise every fact read, expire tasks, propagate deletions/holds and check current corpus/permission epochs after resume. Keep approval records outside model-written memory. A revoked fact in an old summary must not be resurfaced because it remains in a vector memory index. Restore/recovery must preserve revocations. Users can inspect/correct permitted memory; protect cross-user and cross-purpose access.

## “Always valid JSON” at the application boundary

A model is not guaranteed to emit valid JSON on every attempt. The application guarantees that **only a schema-valid result or a schema-valid controlled error is returned**. Use the provider's validated constrained-decoding capability where available, then independently parse with size/depth limits and reject duplicate keys, non-finite numbers, unknown fields and wrong types. Validate status, citation IDs/version/pages and action arguments against current authority.

Use a bounded repair attempt for syntactic errors only; repair cannot add evidence, change grants or execute a tool. On timeout/refusal/invalid content emit a controlled error envelope. A JSON-valid answer can still be factually false or unsafe. The lab validates a bounded answer schema and negative cases, not an enterprise provider's decoder.

For streaming, each SSE event's data is a complete JSON object; buffered final answers undergo schema/evidence validation before the terminal `answer` event. Never pretend arbitrary partially streamed model text is a complete answer object.
