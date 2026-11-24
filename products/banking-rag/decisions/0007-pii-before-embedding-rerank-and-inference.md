# ADR 0007 — PII before embedding rerank and inference

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Privacy, records and model-risk.

## Context

Vectors and reranker input are sensitive too. Uncertain multilingual/image identifiers can bypass a regex.

## Decision

Use restricted extraction plus de-identification before general model paths; keep any OCR-original exception explicit and controlled.

## Alternatives and implications

External raw-document OCR or model processing needs separate approved exposure, never an implicit default.

## Evidence required

Measure detector false negatives by era/script/image; confirm uncertain restricted content cannot bypass admission.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/05-security.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
