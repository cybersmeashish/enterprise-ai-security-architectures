# Evaluation and AI red-team plan

**Implemented:** repeatable authorization, cryptographic admission, HTTP fault, tenant, replay, quota, approval and privacy-fixture tests. A deterministic provider demonstrates that output text does not grant tool authority.

**Unmeasured:** model quality, groundedness, hallucination, demographic fairness, multilingual DLP, refusal behavior and model-level prompt-injection resistance. Transport tests cannot substitute for these.

| Suite | Dataset/procedure | Acceptance evidence |
|---|---|---|
| Authorization | Spoofed tenants, revoked scopes, document ACLs, tool/action replay | Exact allow/deny oracle and no unexpected downstream action |
| Adversarial AI | Direct/indirect injection, poisoned retrieval, tool output, multimodal and encoded attacks | Versioned prompts, expected authority boundary, human review and residual failures |
| Quality | Representative tasks with source-backed reference and blinded reviewers | Cohort distributions, error severity and uncertainty |
| Fairness | Affected populations, language/accessibility and operational cohorts | Approved metrics, legal/context review and mitigation |
| Privacy | Labelled data types, languages, encodings and false-positive/negative cases | Calibrated detector thresholds and governed capture |
| Reliability | Timeout, throttling, malformed output, state outage and cancellations | Attempts, spend, eligible fallback and recovery observations |

Use owned or explicitly authorized environments and synthetic data for public findings. Record model/provider/API/policy/data versions, reviewer, reproducer, expected outcome, actual outcome and limitation. Critical authority failures block release; a mean score cannot erase a high-impact failure.
