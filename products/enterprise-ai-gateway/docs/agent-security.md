# Agent, tool, MCP and A2A security

**Implemented:** the model produces text only. A tool request follows a separate endpoint with a trusted principal, permitted use case, exact schema and tenant-owned asset. Two independent reviewers issue 120-second grants bound to requester, tenant, tool, arguments, policy and use case. Grants are consumed atomically with the synthetic action and completion audit.

**Design:** delegated identity is a distinct subject chain, not text in the prompt. Limit agent task duration, model/tool allowlists, action count, step count, data class and spend. Keep downstream credentials out of model context. Require independent resource authorization at the actual tool service.

MCP and A2A are **not implemented**. For a future remote MCP integration, verify resource identity and audience, use appropriate downstream credentials rather than forwarding a client token, constrain discovery/redirects and prevent a confused deputy. A2A discovery metadata alone does not establish agent trust; validate task scope, identity and endpoint.

Production approval must present the exact consequence and parameters to real reviewers. Revoking a reviewer credential currently prevents issuing new grants, but does not revoke already issued handles; this is an explicit production gap.

[MCP primary guidance](https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices) · [OWASP agentic risks](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
