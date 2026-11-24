# ADR 0018 — Compatible prompt rollback

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Release owner, model-risk and incident owner.

## Context

A bad prompt can harm quality, disclose information or change actions. Cache and in-flight tasks may retain the bad release.

## Decision

Deploy immutable prompt/model/schema/retrieval manifests behind a controlled alias and roll back to a compatible accepted release without restoring revoked permissions.

## Alternatives and implications

Editing a production prompt in place or treating rollback as undoing disclosure is rejected.

## Evidence required

Canary a failing prompt; switch alias, invalidate caches, terminate/review old runs and measure recovery plus incident remediation.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/11-operations.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
