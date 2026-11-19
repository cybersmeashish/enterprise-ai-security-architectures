# Industry patterns and accountable authority

**Stage: synthetic scenarios and design adaptations; no customer deployment or sector compliance is claimed.**

| Sector | Bounded use case | Authority boundary | Next evidence gate |
|---|---|---|---|
| Government | Local public-service procedure assistant | Authorized records; no eligibility or citizen-scoring action | Accountable service owner, jurisdiction applicability and accessibility review |
| BFSI | Internal procedure and transaction-investigation support | Customer entitlements; no lending/payment decision by model text | Customer boundary, transaction approval and model-risk evaluation |
| Oil & Gas | Remote-site maintenance recommendation | OT isolation; two reviewers; recommendation separate from actuation | Real maintenance authorization, safety review and disconnected dependency tests |
| Healthcare | Source-backed document summary | Clinician responsibility; PHI and intended-use control | Clinical validation and privacy review |
| Manufacturing / telecom | Maintenance or incident copilots | IT/OT and network-change approvals | Command/asset authority and failure containment |
| Retail / technology | Support or engineering assistant | Customer/IP isolation; untrusted output | Cohort quality, cache/permission and secure rendering tests |

The fixture has Government, BFSI and Energy principals. Cross-tenant document and asset requests are rejected. The synthetic maintenance action is an SQLite record only.

Connect detailed sector material to [government-security](https://github.com/cybersmeashish/government-security), [bfsi-security](https://github.com/cybersmeashish/bfsi-security) and [oil-gas-security](https://github.com/cybersmeashish/oil-gas-security).

The same gateway contract can be reused; approval rules, data entitlements, evaluation and accountability remain industry-specific.
