# Actual execution evidence — Banking Archive RAG

Executed at `2026-11-24T06:13:08.789992+00:00` inside an OrbStack Linux aarch64 container, allocated four CPU cores and 4 GiB memory. Both source and runtime volume were mounted read-only; only loopback was present and the reserved external-address probe failed with `ENETUNREACH`.

**40 unique regression tests passed**. They exercise assumption-based sizing, schema/error envelopes, synthetic grant/cache/routing boundaries, clause provenance and bounded agent-plan loop checks. **182 local links** and **61 source hashes** were checked.

## Real learned-model ranking experiment

24 synthetic English banking-style texts and 18 author-defined queries/labels. Exact ONNX embedding and cross-encoder artifacts were loaded locally; no answering LLM ran. The labels were not independently adjudicated and the dataset is not a sealed bank holdout.

| Method | MRR@10 | Recall@5 | nDCG@3 | Estimated local path p95 (ms) |
|---|---:|---:|---:|---:|
| bm25 | 0.7917 | 0.9444 | 0.8069 | 0.64 |
| dense | 0.9722 | 1.0000 | 0.9795 | 5.96 |
| hybrid_rrf | 0.8796 | 1.0000 | 0.9107 | 5.97 |
| hybrid_reranked | 0.9306 | 1.0000 | 0.9239 | 99.36 |

Reranking versus hybrid RRF changed MRR@10 by **+0.0509** and nDCG@3 by **+0.0132**; Recall@5 was unchanged. By per-query nDCG it won 2, tied 15 and lost 1. **Dense-only scored higher overall than reranked hybrid** on this small sample. Retain the regression and evaluate on representative bank data before selecting a production policy.

Timing comes from one sequential local run after one warm-up. The hybrid path uses `max(sparse, dense)` as a parallel-path estimate plus measured merge/rerank time. It is not a concurrency benchmark, LLM first-token latency or bank SLA. The reranker added material local latency. No statistical significance or general bank-quality conclusion is asserted.

## Planning outputs and their limits

The six-page, 30-day fixture requires 38.58 admitted documents/second and 231.48 original pages/second on average. With assumed retry/utilisation/OCR values it calculates 561 average OCR workers and 617 capture stations for the separate 26-day, 16-hour capture schedule. These are sizing assumptions, not equipment recommendations or measured capacity.

The generation-cost scenario uses hypothetical prices/cache/routing/token budgets. It does not verify answer quality, complete platform costs or a 70% cost reduction. Thirty customer-support cases are an evaluation specification, not generated support-bot results. Open-LLM serving, scanned-image OCR, Indian-language quality, PII completeness, production authorisation, TTFT and banking compliance remain acceptance work.

## Reproduce and inspect

[Verification](verification.json) · [Planning](planning-results.json) · [Ranking metrics](retrieval-results.json) · [Every query](retrieval-per-query.csv) · [Models/hashes](model-manifest.json) · [Lab observations](lab-observations.json) · [Tests](tests.log) · [Source snapshot](source-manifest.json) · [Lab method](../lab/README.md).
