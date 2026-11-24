# ADR 0017 — Trace each agent without raw PII

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Platform, security and privacy.

## Context

Distributed agents can hide aggregate spend and responsibility; arbitrary model trace tags are not verified identity.

## Decision

Propagate root task scope/budget and child spans through all model/tool/retrieval/validation stages, storing protected payloads only by exception.

## Alternatives and implications

A single orchestrator is preferred until multiple agents demonstrate value. Raw prompt logging is not the default.

## Evidence required

Reconstruct an approved synthetic run, nested retries, cancellation and asynchronous links; test trace ACL/redaction.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/11-operations.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
