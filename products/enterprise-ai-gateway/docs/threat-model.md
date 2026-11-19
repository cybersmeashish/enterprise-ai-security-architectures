# Threat model

**Assets:** tenant documents; workload credentials; approved purpose; policy signer and trust anchors; provider credentials; quotas; action approvals; replay encryption key; audit evidence.

**Boundaries:** client→gateway, identity→claims, reviewer→grant, policy→runtime, gateway→provider, retrieval→tenant document, gateway→synthetic tool, runtime→state/backup. Treat prompts, retrieved text and model output as untrusted.

| Misuse | Enforced boundary | Residual issue |
|---|---|---|
| Forge a tenant or destination | Strict request contract; server principal and model inventory | Real IdP and network admission are future integrations |
| Inject instructions in a retrieved document | Document ACL and classification; tool authorization outside the model | A model may still generate misleading or harmful text |
| Manipulate cost routing | Hard eligibility before price ordering | Model quality is not evaluated by this fixture |
| Outage forces foreign fallback | Same eligibility filters; at most two attempts | Location is declared metadata, not attestation |
| Approve then change tool arguments | Policy/action/requester-bound digest, two reviewers, single use | Real human interface and downstream service not present |
| Replay cached result after revocation | Live identity, policy, model and document checks before replay | No shared cache or distributed revocation proof |
| Delete or rewrite logs | Local hash chain detects ordinary alteration | Tail deletion or privileged recomputation is not externally anchored |
| Restore an old policy/state | Local revision/digest watermark | Full-store rollback needs an independent trusted checkpoint |

Attack tree: unauthorized action can arise through stolen workload scope, malicious approval issuance, replay, changed parameters or downstream authority bypass. The reference tests the first four local boundaries; actual tool services must authorize the resource independently.

See the [25-risk register](../../../examples/risk-register.csv), [20-control map](../../../examples/control-evidence.csv), [tests](../../../tests/test_gateway.py) and [limitations](limitations.md). Findings are synthetic and do not describe vulnerabilities in third-party systems.
