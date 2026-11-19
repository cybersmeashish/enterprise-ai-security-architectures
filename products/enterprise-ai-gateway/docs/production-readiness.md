# Production readiness gate

**Current decision: local security-reference use only. Real-data production use is not approved by this release.**

| Gate | Accountable owner | Required evidence | Current state |
|---|---|---|---|
| Use case and jurisdiction | Business + governance | Intended/prohibited use, applicable obligations, approval | Synthetic record only |
| Identity | IAM | Issuer/audience/signature, federation, rotation and revocation | Demo opaque credentials |
| Network | Cloud/platform | TLS ingress, provider identity, private egress, admin segmentation | Loopback only |
| Data | Privacy/data owner | Classification, real ACLs, DLP calibration, retention and deletion | Fixture checks and replay encryption |
| Model | Model-risk owner | Representative quality, fairness, safety and supplier review | Deterministic fixture |
| Tools | Business/security | Human interface, downstream authority, grant revocation and audit | Synthetic action only |
| State and capacity | Platform/SRE | HA quorum, distributed quota/replay, load/fault tests | Local SQLite; small HTTP cohorts |
| Recovery | SRE/crypto | Separately protected keys, trusted watermarks, restored identity/configuration | Local snapshot tests |
| Evidence | Security operations | External checkpoint, trusted time, retention, access and export | Local metadata chain |
| Supply chain | Engineering | SBOM, reviewed vulnerabilities, trusted builds and provenance | Hash-locked dependencies and CI |
| Service | Product/SRE | Onboarding contract, SLO, support, incident owner and exit exercise | Guide and templates |

Each gate needs an owner, artifact URL, tested version, date, result, residual risk and explicit decision. No average score overrides a failed mandatory safety/authority gate. Record time-bounded exceptions and independent approvers.

[Governance templates](../governance/README.md) · [Known limits](limitations.md)
