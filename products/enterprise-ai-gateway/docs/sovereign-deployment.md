# Sovereign and disconnected deployment patterns

**Stage: architecture guidance plus a network-isolated local fixture.**

| Pattern | Permitted flows | Failure rule | Missing production proof |
|---|---|---|---|
| Connected sovereign site | Site-local processing, explicitly approved provider/private endpoints, controlled support and telemetry | No unapproved external fallback | Observe model, log, backup, key and support placement |
| Intermittent connectivity | Local identity, models, signed policy and durable budget allocation; delayed minimal evidence export | Continue only within current local policy and allocated authority | Offline IdP, actual model dependencies, conflict/reconciliation tests |
| Strict air gap | Local models and dependencies; reviewed offline software/model/policy admission | Reject external routes and stale/untrusted imports | Real update/provenance, local KMS, licensing, DNS/time and recovery validation |
| One-way export | Approved minimal records to a specific recipient, independently verified custody | No reverse commands or unreviewed content | Hardware/network transfer boundary and receiver verification |

Sovereignty includes administrators, provider support, keys, supplier/update control, recovery and organizational authority. A regional gateway or a disconnected network alone does not establish sovereignty.

In this release, an actual Docker run has only loopback interfaces and a failed external-connect probe. Its models are deterministic local HTTP fixtures. This establishes external-network isolation of the test, not the behavior of any real cloud model service.

Use the [disconnected cloud research](https://github.com/cybersmeashish/sovereign-disconnected-cloud-security) for boundary, dependency, admission and recovery evidence, and [sovereign AI](https://github.com/cybersmeashish/sovereign-AI) for related authority patterns.
