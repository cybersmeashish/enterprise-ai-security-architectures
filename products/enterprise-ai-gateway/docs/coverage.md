# Security and governance coverage

This is a broad **32-area coverage map**, not a claim that every AI risk has been solved. New risks enter the register and evidence plan as the product grows.

| Area | Current stage | Inspectable contribution | Next assurance gate |
|---|---|---|---|
| Identity and revocation | Implemented demo | Opaque credentials, scope checks and response-time recheck | Enterprise IdP/audience/federation |
| Tenant and application authority | Implemented | Server principal; no client tenant/endpoint overrides | Real application provisioning |
| RAG resource entitlement | Implemented fixture | Tenant/subject ACL and class escalation | Real index and source authorization |
| Policy integrity and rollback | Implemented | Ed25519 site/revision/digest checks | Protected signer; independent recovery watermark |
| Model/use-case lifecycle | Implemented | Approved state and review expiry | Actual supplier and model-risk review |
| Data classification | Implemented | Highest trusted floor and document class | Organization-specific classification |
| PII, secrets and DLP | Fixture only | Narrow regex positive/negative cases | Multilingual calibration; obfuscated text gap |
| Residency and sovereignty | Declared constraint + design | Region-filtered fixture routing | Observed inference/log/key/support placement |
| Provider credentials | Implemented fixture | Dedicated upstream token; no bearer forwarding | Vault/federation, TLS and rotation |
| Network/SSRF | Implemented local restriction | Literal loopback endpoint; no redirect following | Real private egress and destination identity |
| Tool authorization | Implemented synthetic action | Tool schema, asset ownership and two reviewers | Real service authorization and approval UI |
| Delegation and MCP/A2A | Design | Agent authority contract | Protocol conformance and audience-bound exchange |
| Budget and rate safety | Implemented | Transactional credit reservation and attempt limits | Real usage/billing and HA invariants |
| Idempotency and caching | Implemented local | Tenant/subject scoped encrypted 30-second replay | Durable leases, crash recovery and shared state |
| Response encryption | Implemented | AES-GCM; key-loss/backup tests | KMS, rotation and separately protected restore |
| Audit privacy/integrity | Implemented with known gap | Metadata-only local hash chain | External anchor, custody, access and time assurance |
| Retention and deletion | Partial logical TTL | Expired completed replay records removed on a later claim | Physical erasure, backups and scheduled deletion |
| Provider failure and fallback | Implemented fixture | Timeout, response validation, two attempts and circuit | Real inference/cancellation/streaming |
| Observability and SIEM | Local metadata + design | Stable reasons and audit records | Export, alerts and current semantic conventions |
| Governance records and ownership | Implemented validator | 25 risks, 20 control links, owners and exception expiry | Accountable real decisions |
| Privacy/regulatory applicability | Assessment design | Privacy and applicability worksheets | Qualified jurisdiction-specific review |
| Model quality and fairness | Design; unmeasured | Representative evaluation contract | Learned-model datasets and cohort results |
| Red teaming and abuse testing | Implemented boundaries + plan | Adversarial contract tests and known failures | Real-model/multimodal campaigns |
| Model/data supply chain | Partial + design | Dependency lock and registry ownership | Model provenance, quarantine and independent vulnerability review |
| Prompt/system-instruction secrecy | Design | No authority or secrets entrusted to model text | Application and learned-model leakage tests |
| Multimodal/embeddings/reranking | Roadmap | Text-only strict API rejects unsupported fields | New explicit contracts and media tests |
| HA/distributed state | Design | Federated architecture and partition invariants | Quorum/partition and recovery experiments |
| Capacity and large-scale operation | Measured small fixture | 180 HTTP requests across 3 cohorts | Representative long-duration enterprise loads |
| Incident response and recovery | Local tests + playbook | Credential, model, key and snapshot cases | End-to-end incident and actual identity/provider recovery |
| FinOps and business outcomes | Synthetic meter + design | Reserved byte credits and business case | Provider reconciliation and useful-task economics |
| Post-quantum transition | Inventory/design | Signature/key-establishment dependency distinction | Maintained PQ implementation interoperability |
| Human safety and affected people | Design | Prohibited use, human oversight and review records | Stakeholder/impact and sector-specific evaluation |

[Implementation-to-test records](../../../examples/control-evidence.csv) · [Risk register](../../../examples/risk-register.csv) · [Production gate](production-readiness.md)
