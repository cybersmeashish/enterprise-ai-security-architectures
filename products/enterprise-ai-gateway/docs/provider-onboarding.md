# Provider onboarding and comparison scorecard

**Stage: design/evaluation worksheet.** No real provider integration or vendor ranking has been performed.

| Mandatory gate | Evidence to request/test | Reject if |
|---|---|---|
| Identity and secrets | Destination/audience, credential rotation, private identity and no user-token pass-through | Tokens can be confused across resources |
| Data and location | Processing, logs, retention, backups, support access and subprocessor terms | Contract or observed path conflicts with the use case |
| Protocol correctness | Input/output limits, streaming semantics, tools, usage and error taxonomy | Silent approximation can change business behavior |
| Resilience | Timeout/cancel, ambiguous outcomes, throttling, retries and fallback | Failover escapes hard policy constraints |
| Governance | Model version, intended use, provenance and evaluation evidence | Model lifecycle or approval is unowned |
| Exit and commercial fit | Export, portability, cancellation, data deletion and cost per task | No verifiable exit or unacceptable terms |

Compare candidates only after these gates. Record product/version/edition, source/date, documented capability versus your test, environment, result and reviewer. Do not reuse a vendor feature list as independent validation.

The local adapter accepts only literal loopback endpoints and never follows a redirect. A future provider adapter must add destination identity, TLS, egress controls, provider-specific credentials and explicit capabilities.
