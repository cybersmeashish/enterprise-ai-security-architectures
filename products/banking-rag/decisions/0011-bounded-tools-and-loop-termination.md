# ADR 0011 — Bounded tools and loop termination

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Application/service owners and CISO.

## Context

Repeated calls or a timeout can duplicate effects; untrusted text cannot become a tool recipient or approval.

## Decision

Use allowlisted schema-validated tools, independent grants, idempotent effects and cumulative step/cost/time budgets.

## Alternatives and implications

Unrestricted SQL, shell, web navigation and self-approved financial actions are outside the first release.

## Evidence required

Force same-state loops, transient/permanent failures, timed-out writes, cancellation and denied action proposals.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/09-agents-memory-json.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
