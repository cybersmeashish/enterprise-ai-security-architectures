# ADR 0005 — Clause-aware legal chunking

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** Records/legal and retrieval lead.

## Context

Fixed windows can sever a notice rule from its exception or a table row from its units. Initial token budgets must be measured.

## Decision

Use structured clause children with authorised parent/definition/exception expansion and page-coordinate citations.

## Alternatives and implications

Fixed windows remain a fallback for low-structure material, with explicit loss/uncertainty flags.

## Evidence required

Measure gold clause/context recall, amendment precedence, oversized-clause split and original-page hydration.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/04-chunking-retrieval.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
