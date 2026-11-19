# Identity, application and tenant boundaries

**Implemented:** random opaque credentials, hashed in-memory lookup, expiry and revocation. A server-issued Principal fixes subject, tenant, use cases, scopes and role. The client cannot lower its tenant or authority through metadata. Identity is checked before idempotency replay, before each provider attempt and after the response.

**Target contract:** an enterprise IdP validates issuer, audience, signature, expiry, not-before and scopes; workload identity distinguishes human, application, service and agent. Administrative policy changes use separate roles and accountable approval. Do not mistake an API key for the human user's business authority.

No OIDC discovery, JWT validation, token exchange, federation or device trust is implemented. The demo issuer exists only to exercise local authorization. Use RFC 9700 and NIST SP 800-207 as design references, and verify current IdP behavior in your deployment.

Tests include wrong scope, expired/revoked token, revocation during provider execution, server tenant derivation, tenant/subject-separated replay and cross-tenant document access.

[Primary references](../../../references/README.md) · [Agent delegation design](agent-security.md)
