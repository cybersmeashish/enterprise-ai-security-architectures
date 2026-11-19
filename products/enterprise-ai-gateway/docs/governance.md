# AI governance operating system

**Implemented:** a validation tool checks the original synthetic record contract, model/use-case references, ownership, exception expiry and control/artifact/test links. Runtime policy enforces reviewed purpose/model state and expiry. Validating an example does not establish real review or certification.

```sh
.venv/bin/python -m tools.validate_governance examples/governance-pack.json
```

| Lifecycle decision | Accountable owner | Record and evidence |
|---|---|---|
| Why use AI? | Business product owner | Intended outcome, prohibited decisions, affected people and baseline |
| Which data? | Data/privacy owner | Source authority, entitlements, classification, processing and deletion |
| Which model/provider? | Model-risk + supplier owner | Model card, supplier terms, location, version, representative evaluation |
| Which authority? | IAM/security + process owner | Subject, delegated scope, tool bounds, exact human approvals |
| Which release? | Platform + independent approver | Signed policy, tested change, canary/rollback and expiry |
| Which operational conclusion? | SRE/evidence owner | Current measurements, evidence freshness, failures and uncertainty |
| Which risk remains? | Accountable executive/governance | Residual-risk decision, exception scope, compensating control and expiry |

The [governance pack](../../../examples/governance-pack.json) contains synthetic use cases, model records, 25 risk entries, 20 traceable control records, an example exception, operating owners and an evaluation plan. Owner names are role examples, not people who have approved this product.

Use the [14 working templates](../governance/README.md) for onboarding, supplier/model review, privacy, evaluation, risk, changes, exceptions, actions, incidents, capacity, economics and board reporting.

NIST's Govern/Map/Measure/Manage functions provide a useful organization for the evidence; the gateway is one enforcement component inside a larger management system. Jurisdiction, intended use and organizational role determine applicable legal obligations. Have an accountable qualified reviewer make that determination.
