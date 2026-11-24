# 03 — Physical archive, ingestion and the 100M/month target

A document is not a page and a page is not a chunk. Separate **physical capture capacity**, **digital processing capacity**, **index admission** and **interactive inference**. The lab calculator reports each with editable assumptions; it does not benchmark a production platform.

## Preserve and prepare century-old records

Survey samples by era, branch, language/script, handwriting, paper condition, page size and document class. Records managers decide whether fragile volumes can be unbound, flattened or scanned; conservation work is not included in scanner-rated speed. Photograph custody and missing-page anomalies. Record the true capture date separately from the historical document date. Cryptographic hashes prove later byte consistency, not authenticity of the original paper.

Use calibrated, approved archival capture settings (resolution/colour depend on material), page/folio sequence checks and double-entry review for key identifiers and amounts. Treat receipts and tables as layout objects; a cell shifted into another column can create a financially wrong answer despite apparently readable OCR. Use tested language-specific OCR/handwriting paths and retain word boxes, confidence, alternative readings and original crops. Low confidence, broken clause references, illegible amounts, suspicious amendments and missing pages cause quarantine or explicit human review. OCR confidence is not answer confidence.

## Reference sizing inputs and equations

For a 30-day calendar month: `DPS = documents / (30 × 86400)`. `PPS = DPS × mean_pages`. `processed_PPS = PPS × retry_amplification`.

An OCR worker processing one page in `s` seconds at usable utilisation `u` contributes `u/s` pages per second. Required workers are `ceil(processed_PPS × s/u)`, separately for average and burst. Measure `s` per document stratum and bound p95 queues; one average hides handwriting and large tables.

For physical capture, `stations = ceil(pages / (capture_days × hours/day × 60 × rated_pages/minute × usable_utilisation))`. This includes only the assumed operating schedule and scanner utilisation. Handling, conservation, QA, re-scans and staff coverage must be added from a real capture study.

`embedding_tokens = pages × tokens/page × retry_amplification`; `chunks = documents × measured_chunks/document`. Vector-only bytes are `chunks × dimensions × bytes/value`. Add index overhead, replicas, sparse index, text, metadata, tombstones and retained generations separately. Original image bytes are usually a much larger line item. GB/TB in the calculator are decimal units.

The reference six-page scenario produces 600M pages and 800M chunks per planning month. The [actual calculator output](../evidence/planning-results.json) records required rates, workers, scanner stations and storage under the fixture assumptions. No ingest throughput is claimed.

## Pipeline design constraints

- Partition by region/site and bank-approved security boundary, then hash document ID for workload balance. Do not shard only by customer name or leak it into a queue key.
- Apply backpressure before an expensive stage. Token buckets regulate OCR, embedding and index writes; offline migration may yield to online service quotas.
- Use a content hash for duplicate detection plus logical document/version identity. Two identical pages attached to different authorised cases retain separate grants and provenance. A rescan with changed OCR is a new derivative version.
- Persist stage offsets, errors, retries and reconciliation totals. A poison document enters a dead-letter queue without blocking its batch. Controlled replay cannot count the same admitted document twice.
- Bulk-build a versioned index, verify parity and grants, then atomically switch the serving alias. Keep a known-good generation until rollback is approved. Permission revocation applies to every retained generation.
- Do not send every page to a general-purpose LLM for extraction. Use deterministic parsing/OCR first, bounded specialist models for difficult cases and human review for material uncertainty.

## Measurement plan

Use separate 10K-document calibration, 1M-document pilot and sustained-load stages before accepting 100M/month. Stratify rather than cherry-pick clean scans. Measure accepted unique documents/hour, pages/hour, error/review fraction, queue-age p95/p99, time-to-searchability, recovery headroom, duplicate rate and cost per admitted document. Confirm no exhausted queue or retry path drops custody/ACL data. Treat physically unavailable originals and rights gaps as business blockers, not engineering success counts.
