# Local API contract

**Stage: implemented, loopback-only HTTP demonstration.** No vendor SDK compatibility or OpenAI API compatibility is claimed.

| Endpoint | Authority | Contract |
|---|---|---|
| `GET /healthz` | No credential; no sensitive state | Process liveness only, not readiness |
| `POST /v1/generate` | `generate` scope and approved use case | Required `use_case`, `prompt`, `max_output_bytes`; optional higher `classification`, permitted `document_id` |
| `POST /v1/approvals` | Independent `reviewer` with `approve` scope | Exact action and intended requester; returns a 120-second synthetic grant |
| `POST /v1/tools/invoke` | `invoke` scope, permitted tool and owned asset | Exact action with two distinct reviewer grants |

POST bodies require exactly `application/json`, one content length and one bearer header. Transfer encoding, duplicate JSON keys, NaN, arbitrary fields, oversized bodies and invalid identifiers are rejected. Generate requires an `Idempotency-Key` of at most 80 permitted characters. Credentials are verified before JSON parsing.

The response contains text, selected model, declared region, policy hash/revision, attempt count and the synthetic metering label. Errors return stable codes such as `scope_denied`, `document_access_denied`, `no_eligible_model`, `budget_exhausted`, `invalid_action_approval` or `provider_invalid_response`.

Output is **untrusted JSON data**. A consuming browser must escape/sanitize before rendering; this gateway does not make HTML safe.

Only `maintenance.schedule` is supported, and it records an action in a synthetic SQLite table. It never changes real assets. There is no network administration endpoint, production IdP, remote provider adapter, MCP or A2A protocol server.
