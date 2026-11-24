# ADR 0009 — Semantic cache with scoped reuse

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Security, retrieval and SRE.

## Context

Cosine similarity is not identity, authorization or query equivalence. Numbers and negation must match.

## Decision

Cache only eligible low-risk answers inside matching subject/case/purpose/permission/corpus/release scope with freshness checks.

## Alternatives and implications

A cross-customer global answer cache is rejected; exact authorised service caching is a separate design.

## Evidence required

Track hit/total and hit/eligible; test epoch/release/entity changes, invalidation, expiry and grants on every hit.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/08-cost-latency.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
