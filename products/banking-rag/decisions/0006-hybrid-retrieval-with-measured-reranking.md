# ADR 0006 — Hybrid retrieval with measured reranking

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Retrieval lead and model-risk.

## Context

Exact identifiers and semantic paraphrases have different failures. A cross-encoder can regress or miss a truncated exception.

## Decision

Default the mixed archive to authorised hybrid retrieval; admit a bounded reranker only where paired gains justify cost and tail latency.

## Alternatives and implications

BM25, dense-only and exact lookup remain valid task-specific alternatives. Do not assume hybrid wins all benchmarks.

## Evidence required

Compare BM25/dense/RRF/rerank on identical sealed queries; retain every per-query regression and language gap.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/04-chunking-retrieval.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
