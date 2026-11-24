# 08 — 70% cost target, semantic cache, routing and first-token latency

## Cost target with a quality constraint

The target is **at least 70% lower cost per acceptable answer** on a representative paired workload without a material quality/safety regression. Separate LLM token cost from OCR, embedding, search/rerank, GPU idle capacity, cache/storage, networking, review staff and migration cost. Provider prices in the lab are explicit hypothetical rates; they are not current commercial quotes.

Begin with a measured baseline. Remove repeated context, use clause/parent selection instead of entire documents, request task-appropriate concise output, use exact authorised lookups, cache eligible low-risk answers and route easy supported questions to a smaller model. Batch noninteractive ingestion independently. Do not reduce necessary legal context or change answer completeness merely to report savings.

The fixture calculator reports baseline and proposed generation spend and savings. It does not generate answers or demonstrate unchanged quality. The [acceptance plan](acceptance-plan.md) defines a paired quality/safety gate and a complete cost boundary before the 70% target can be called achieved.

## Semantic cache design and hit-rate tracking

Use semantic matching only for **eligible, low-risk, evidence-grounded** answers. Account balances, transaction status, individual customer entitlements, material legal conclusions and sensitive agent actions default to no answer-cache reuse. A deterministic authorised ID lookup may still be cached in its own service under strict freshness rules.

Cache scope includes bank/tenant, subject-or-approved share group, purpose, customer/case, permission epoch, corpus/index version, policy version, model/prompt/schema release, language, time/as-of window and query entities. Compare an embedding only within this scope. Require an initially conservative similarity threshold (0.97 is a tunable starting hypothesis), exact important entities/numbers/negation/as-of checks, supported citations and a short TTL. A high cosine score never grants permission or proves equivalence.

Before returning a hit recheck the subject's current grant and every cited document version; invalidate by permission/corpus/prompt epochs and deletion events. Encrypt entries, constrain retention and avoid raw identifiers in keys. Treat cached model output and cache poisoning as security risks. A cross-user sharing group needs explicit policy, not just matching text.

Track total requests, eligible requests, actual cache probes, valid hits, semantic candidates rejected, expiries, invalidations and stale/security blocks. Report **hit/total** and **hit/eligible** separately alongside cost avoided and measured quality of hits. Prevent denominator gaming by counting ineligible requests. The lab exercises scope/version/expiry rejection and counters; it is an in-memory boundary demonstration, not a scalable production vector cache.

## Cheap versus smart model routing

Route from trusted risk/task features, evidence sufficiency, supported language, token budget and actual task evaluation. Exact retrieval/formatting with strong evidence may use a cheap model. Ambiguous legal clauses, OCR uncertainty, conflicts, unsupported language or material financial conclusions need a validated stronger model or human review. “Smart” does not waive evidence or safety requirements. Missing authorization always denies; missing evidence does not automatically become an expensive hallucination.

Set a fallback budget and deadline; allow at most a bounded escalation. Calibrate routing thresholds on held-out outcomes and track selection bias. User instructions cannot label a task low-risk or select an unapproved external model. Preserve identical privacy and output checks on both paths.

## Cut first-safe-token latency

Measure first **safe visible** content separately from network heartbeat, retrieval events, model first token and full completion. Retain end-to-end p50/p95/p99 under representative concurrency. The proposed interactive objective starts at p95 ≤1.2 seconds for eligible cache/exact-lookup queries; uncached deep legal research has a separate SLO rather than an unachievable universal promise.

Reduce queueing with admission control, warm capacity, bounded context, parallel independent sparse/dense search, colocated approved components and measured reranker scope. Use provider/model prefix reuse only when isolation permits; it cannot replace a retrieval/permission recheck. Quantization and smaller models require quality tests. Streaming improves perceived latency but cannot fix a slow first token or safely reveal text before required checks. Never label a heartbeat as a faster answer.
