# Disruption and security incident playbook

**Synthetic exercise:** revoke workload credential; suspend model/use case; reject unsafe fallback; preserve source policy and metadata evidence. Assign incident commander, security, data, platform and business owners.

For stolen credential: revoke identity/grants, contain tenant, inspect minimal audit, rotate affected provider secrets and review approvals. For malicious output/import: suspend affected model/policy, preserve hashes, avoid amplifying sensitive content and reassess evaluation. For state/region outage: fail closed or use only pre-authorized local authority.

Record observed times with clock confidence, business impact, action owner, evidence custody, recovery, missed detections and next control. Exercise real identity, model and key recovery before claiming readiness.
