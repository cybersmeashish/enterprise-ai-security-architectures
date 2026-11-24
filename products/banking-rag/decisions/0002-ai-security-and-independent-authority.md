# ADR 0002 — AI security and independent authority

**Status:** adopted for the reference; production implementation/acceptance pending.

**Owners:** CISO and service owners.

## Context

User text, retrieved material and tool results may contain instructions. Trusted identity and permissions must originate outside those channels.

## Decision

The LLM can propose but cannot create grants, approve actions or choose unrestricted tools/recipients.

## Alternatives and implications

Prompt-only guardrails are insufficient; universal agent access is rejected.

## Evidence required

Inject a malicious clause and prove no customer scope, action grant or export recipient changes.

The current repository establishes design intent and explicitly bounded lab evidence. It does not establish this decision's implementation in a bank.

[Detailed design](../docs/05-security.md) · [Acceptance gates](../docs/acceptance-plan.md) · [Source context](../docs/12-source-guide.md).
