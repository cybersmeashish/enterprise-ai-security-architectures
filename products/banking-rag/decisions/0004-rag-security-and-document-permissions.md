# ADR 0004 — RAG security and document permissions

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Data owner and identity service.

## Context

A generated answer can leak a denied document even if the UI hides its title. Stale indexes and restores can resurrect revocations.

## Decision

Apply trusted grants before sparse/dense candidates and recheck parent expansion, cache, citations and display.

## Alternatives and implications

A global index plus post-generation redaction alone is rejected. Physical index partitions may augment filters.

## Evidence required

Deny cross-case probes, stale epochs, count/score leakage, parent expansion and cached answers after revocation.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/05-security.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
