# ADR 0016 — SSE safe output and disconnects

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Application and SRE.

## Context

Raw token streaming may disclose unsupported content before validation; reconnect can replay stale sensitive data.

## Decision

Emit complete JSON events; distinguish progress from first safe answer; cancel or budget background work and reauthorise reconnect replay.

## Alternatives and implications

Buffered high-risk answers are acceptable even when slower. Heartbeats are not answer-latency improvements.

## Evidence required

Test disconnect, expired cursor, revoked grant, proxy buffering, partial stream and idempotent run creation.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/11-operations.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
