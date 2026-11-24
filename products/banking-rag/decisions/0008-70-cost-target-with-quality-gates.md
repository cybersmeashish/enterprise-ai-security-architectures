# ADR 0008 — 70 percent cost target with quality gates

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Business, FinOps and model-risk.

## Context

Assumed token prices and shorter context can create apparent savings while losing material evidence.

## Decision

Optimize complete cost per acceptable answer only after a paired baseline and predefined quality/safety noninferiority gates.

## Alternatives and implications

Pure token-cost minimisation or changing the workload denominator is rejected.

## Evidence required

Record total cost, paired expert outcomes, adverse strata, abstention and privacy/material failures; independently accept.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/08-cost-latency.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
