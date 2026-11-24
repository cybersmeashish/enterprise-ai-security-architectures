# ADR 0013 — Schema-valid application JSON

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Application owner and security.

## Context

Constrained generation can refuse or fail, and valid JSON can still contain unsupported claims.

## Decision

Return only independently validated answer envelopes or controlled error envelopes; separately validate citations and authorization.

## Alternatives and implications

Unbounded repair and blindly parsing arbitrary model output are rejected.

## Evidence required

Reject duplicate keys, non-finite numbers, unknown fields, denied citations, empty evidence and oversized output.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/09-agents-memory-json.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
