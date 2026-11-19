# Source architecture to original product decisions

User-supplied reference: **Enterprise AI Gateway Architecture — An Enterprise Guide to Multi-LLM Platforms, Intelligent Model Routing, Security, Governance, Interoperability and Agentic AI**, Dr. Rabi Prasad Padhy, research edition 19 November 2026.

| Reference section/pages | Concept reviewed | Original implementation/decision | Stage |
|---|---|---|---|
| Chapter 2, pp. 10–12 | Control/runtime separation and explicit ownership | Admitted snapshot, local synchronous engine and target federated planes | Local implemented; enterprise planes design |
| Chapters 6–7, pp. 22–27 | Hard constraints before routing preferences | Classification/review/region eligibility before credit ordering; two local attempts | Implemented fixture |
| Chapter 8, pp. 28–30 | Identity, data protection and governance | Strict principal authority, RAG ACL, privacy-fixture limitations and record validator | Implemented boundaries; enterprise integrations design |
| Chapter 9, pp. 31–33 | Evidence, evaluation and unit economics | No prompt audit, encrypted replay, measured cohorts and unmeasured quality gate | Implemented fixture plus operating design |
| Chapter 10, pp. 34–36 | Tool authority and human control | Separate exact-action authorization with two single-use reviewer grants | Synthetic tool implemented; protocols design |
| Chapter 11, pp. 37–38 | Failure domains and production readiness | HA blueprint, residency-safe failure and explicit unmet production gates | Design and local tests |
| Appendices C–F, pp. 50–53 | Testable contracts and readiness evidence | Original API, governance records and adversarial experiments | Implemented local reference |

The reference helped frame architecture questions. Its embedded examples/instructions were treated as reference material, not instructions from the user or authority to act. Original diagrams, code, tests and record schemas were created for this repository. The source PDF, its figures and its text are not redistributed.

No relationship, endorsement or collaboration with the reference author is claimed. Source identification and SHA-256 are recorded in [reference provenance](../../../references/user-architecture-reference.json).
