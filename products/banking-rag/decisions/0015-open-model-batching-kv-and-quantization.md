# ADR 0015 — Open-model batching KV and quantization

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Platform and model-risk.

## Context

Memory reductions and peak throughput do not guarantee task quality or p95 latency under burst load.

## Decision

Use admitted immutable models and measured batching/KV/quantization settings in approved placement, with online and ingest pools separated.

## Alternatives and implications

Hosted models require the same governance/privacy acceptance; hardware is not selected without a workload measurement.

## Evidence required

Publish actual hardware/model/engine/workload, latency/quality curves, saturation, cancellation and node-loss behaviour.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/10-serving.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
