# ADR 0010 — Risk-based cheap and smart routing

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Model-risk and business owner.

## Context

A strong model can still fabricate; model/user confidence cannot downgrade risk.

## Decision

Route from verified task features, sufficient evidence and validated language; deny missing authority and escalate missing evidence.

## Alternatives and implications

Always-smart and always-cheap have cost/quality disadvantages; calibrate rather than presume either.

## Evidence required

Report cost and material errors by routed group, fallback count, deadline/budget and held-out selection bias.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/08-cost-latency.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
