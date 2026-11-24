# Acceptance gates — evidence required before production claims

| Gate | Required measurement | Responsible acceptance |
|---|---|---|
| Archive readiness | Custody/rights survey, capture-condition strata, missing pages and retention decisions | Records owner and legal/privacy |
| 100M/month | Sustained admitted unique document/page rates, stage queues, QA/retry fraction, headroom and restore/replay under representative scans | Platform, records and business owner |
| Retrieval | Held-out recall/ranking by language/era/task; permissions and temporal tests; reranker paired deltas and tail cost | Retrieval lead and model-risk |
| Answer quality | Human-labelled material error, unsupported claims, supported citations, abstention/false refusal and case isolation | Business, legal and model-risk |
| 70% cost reduction | Paired complete cost per acceptable answer; quality noninferiority margin predefined; no privacy/material-risk regression | Business, FinOps and model-risk |
| First-safe-token latency | End-to-end p50/p95/p99 by cache/uncached task class at accepted arrival rate and overload | SRE and business owner |
| Security/privacy | Denied retrieval/cache/citation/tool cases, PII recall by stratum, injection and parser isolation; unresolved findings | CISO and privacy |
| India applicability | Latest directions, entity scope, commencement dates, contracts, transfer/retention duties and incident obligations pinned | Legal/compliance and outsourcing owner |
| Operation | Clean restoration, permission tombstones, cancellation/reconnect and compatible prompt rollback exercise | SRE, CISO and incident owner |

Set quantitative quality thresholds only after a baseline and representative sampling. “Zero failures observed” in N cases is not proof of zero probability. For rare safety events report uncertainty and sample size; escalation/abstention is part of the service contract.

Suggested sequence: 10K-document calibration → 1M representative ingestion pilot → protected staff shadow use → canary with accepted evidence → staged regional scale. Timing and staffing depend on capture capacity, legal rights and observed failures; no fixed delivery promise is inferred.
