# ADR 0012 — Long-running memory is evidence not policy

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Privacy, identity and application owner.

## Context

A summary may preserve a revoked fact or an injected instruction. Model-written memory cannot hold authoritative grants.

## Decision

Separate session/task facts and durable verified memory; reauthorise and revalidate provenance/expiry on every resume.

## Alternatives and implications

An unscoped vector memory shared across users is rejected.

## Evidence required

Revoke a remembered source, restore an old snapshot, change purpose and test deletion/hold handling without leaks.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/09-agents-memory-json.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
