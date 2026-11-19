# FinOps and business value

**Implemented:** worst-case synthetic credits are reserved transactionally per tenant before each provider attempt. Cost ranking occurs only after hard authorization, classification, review and declared-region checks. Failed/ambiguous attempts remain charged; replay does not create a second provider call.

These credits use byte counts and fixture prices. They are neither tokenizer counts nor currency. Provider usage, discounts, invoicing, caching and refunds are not implemented.

For a pilot, measure cost per successful **business task**, including inference, gateway/state, retrieval, tools, security checks, telemetry, support and human review. Compare against the same task without the gateway. A lower model price can still increase rework.

| Record | Required fields |
|---|---|
| Allocation | Tenant, application, use case, cost center, owner and budget period |
| Attempt ledger | Model/version, provider, actual usage, reservation, outcome and ambiguous-cost handling |
| Task outcome | Accepted/rejected/reworked, source evidence, human review and cohort |
| Unit economics | Total allocated cost, successful task denominator, uncertainty and comparison conditions |

Do not claim ROI or revenue gains before a measured pilot. Use [FinOps unit economics](https://www.finops.org/framework/capabilities/unit-economics/) as a reference and the [business case template](../governance/business-case.md) to define the hypothesis.
