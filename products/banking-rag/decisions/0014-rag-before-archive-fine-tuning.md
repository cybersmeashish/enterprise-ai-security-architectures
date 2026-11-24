# ADR 0014 — RAG before archive fine-tuning

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Records, privacy and model-risk.

## Context

Weights are a poor primary mechanism for document versions, per-customer access and deletions. RAG still requires groundedness checks.

## Decision

Keep changing customer facts in versioned authorised retrieval; use prompts for behaviour and consider narrow fine-tuning only for measured task gaps.

## Alternatives and implications

Fine-tuning is not forbidden for legitimate tasks; it must not replace knowledge rights or fix an ACL failure.

## Evidence required

Compare retrieval/context versus behaviour failures; approve training rights and evaluate a fine-tune only with a defined gap.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/10-serving.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
