# Framework-to-evidence mapping

**Stage: selected interpretive assessment aid.** This is not an exhaustive control catalog, legal opinion, certification or official framework endorsement.

| Reference | Selected concern | Local evidence | Unresolved assessment work |
|---|---|---|---|
| NIST AI RMF — Govern | Ownership, purpose, review and exceptions | Governance pack, policy/model review expiry, record validator | Actual organizational policies and accountable approval |
| NIST AI RMF — Map | Context, affected people and dependencies | Threat model, industry cases, intended/prohibited-use records | Real stakeholders, jurisdiction and consequence analysis |
| NIST AI RMF — Measure | Testing and uncertainty | 92 regression tests, 12 scenarios, synthetic HTTP cohorts, explicit gaps | Learned-model quality/fairness/privacy, representative populations |
| NIST AI RMF — Manage | Mitigation, suspension and recovery | Eligibility, expiry, local fallback, revocation and snapshot tests | Production treatment decisions, independent checkpoints and incidents |
| NIST Generative AI Profile | GenAI-specific risk analysis | Risk register, red-team plan, retrieval/tool boundaries | Broader lifecycle and socio-technical risk assessment |
| NIST SP 800-207 | Per-request authority | Trusted principal, scope, tenant and resource checks | Enterprise IdP, device/workload posture and continuous verification |
| RFC 9700 | Audience-bound authorization and OAuth deployment | Provider fixture has its own credential; caller bearer is not forwarded | Actual OAuth implementation and conformance testing |
| OWASP LLM Top 10 2025 | Application/LLM risk categories | Mapping below | Real-model, ingestion and consumer application assurance |
| OWASP agentic Top 10 2026 | Agent trust and action containment | Model proposals cannot authorize actions; bounded two-reviewer grants | MCP/A2A, real delegation and downstream services |
| ISO/IEC 42001 | AI management system context | Management-system-oriented records and ownership | Full standard and clauses were not reviewed; independent requirements assessment |
| SLSA v1.1 verification guidance | Trusted artifacts/build evidence | Hash-locked dependencies, policy signature tests and source manifests | SLSA provenance and builder verification are not implemented |

## OWASP LLM Top 10 — release scope

| Category | Gateway contribution | Remaining responsibility |
|---|---|---|
| LLM01 Prompt Injection | Retrieval ACL and deterministic action authority | Learned-model behavior, source controls and adversarial evaluation |
| LLM02 Sensitive Information Disclosure | Class floor, eligible routes, privacy fixtures, no prompt audit | Calibrated DLP, provider processing, real retention/deletion |
| LLM03 Supply Chain | Dependency hashes, model registry, signed policy | Software/model provenance, vulnerabilities, trusted build and supplier review |
| LLM04 Data and Model Poisoning | Record-based model and document ownership | Ingestion/training integrity and poisoning evaluation |
| LLM05 Improper Output Handling | Strict JSON response shape/size; no automatic code execution | Safe rendering, SQL/command handling and downstream validation |
| LLM06 Excessive Agency | Scope, tool/asset allowlists, two exact-action grants | Real service authority, agent step limits and human interface |
| LLM07 System Prompt Leakage | Secrets/authority are kept outside fixture prompts | Application prompt exposure and real-model tests |
| LLM08 Vector and Embedding Weaknesses | Subject/tenant document ACL example | Real index isolation and permission reconciliation |
| LLM09 Misinformation | Evaluation and human oversight contract | Groundedness/factuality and representative human review |
| LLM10 Unbounded Consumption | Size, concurrency, attempt rate and budget limits | Distributed state, ingress protection and production capacity |

The framework labels come from the primary sources; the mapping and judgments are original interpretation. See [source metadata](../../../references/primary-sources.json). ISO's public overview was reviewed for scope only; no paywalled requirements are reproduced.
