# 07 — Debug wrong answers, hallucinations and evaluation

## Debug by finding the first broken link

Use an approved, redacted trace ID to inspect **capture → OCR → structure/chunk → permissions/version → retrieval → rerank → context → generation → validation → display**. Preserve the exact model, prompt, schema, tokenizer, index generation, grant epoch and corpus version. Raw PII is not required in ordinary traces; restricted evidence inspection needs separate access.

| Symptom | First diagnostic | Corrective experiment |
|---|---|---|
| Wrong amount/date/name | Original crop, OCR alternatives, table row/header and mapping | Compare corrected OCR against original; require review for material ambiguity |
| Correct clause, wrong legal conclusion | Definition, exception, schedule and amendment linkage | Parent/context expansion and temporal precedence; legal reviewer adjudicates |
| No answer despite relevant source | Gold clause in authorised corpus, recall@K, query translation | BM25/dense/union ablation; fix missing source before changing prompt |
| Confident obsolete answer | Effective/superseded dates and selected corpus snapshot | Current-policy precedence and conflict/abstention case |
| Wrong customer's information | Grant filtering, hydration/cache scope and epochs | Treat as an incident; suspend path, reproduce with synthetic identities |
| Hallucinated citation | Source ID/version/page exists and supports exact claim | Reject unsupported claim; bounded repair or human escalation |
| Slow first token | Queue wait, retrieval/rerank, prefill, connection and buffering spans | Tune the measured bottleneck rather than blindly shrinking output |

Retain both successful and failing replay cases. Change one variable at a time or use a declared factorial experiment. If source evidence is unreadable or conflicting, the system should say what is missing; forcing a fluent answer is not a fix.

## Detect and reduce hallucinations

Require a claim-to-citation structure. Verify authorised source identity, version, page/coordinates, recency and lineage. Deterministically verify calculable amounts/dates where possible. Use a groundedness assessor only as supporting evidence; semantic entailment models and judges can miss contradictions. A citation can exist without supporting the claim. Limit answers to supplied evidence, surface conflicts and unsupported parts, and abstain/escalate when the context is insufficient. Independent checks should inspect both the cited clause and necessary exceptions.

Measure unsupported-claim rate, correct citation support, material factual error, safe abstention, false refusal and cross-customer leakage. Avoid “hallucination = zero” claims from small samples. Split retrieval failures from synthesis failures and OCR failures so the right team can act.

## Customer-support bot evaluation suite

The fixtures define a synthetic support evaluation specification, including answerable questions, unavailable evidence, version conflicts, exact identifiers, redacted PII, access denial, injections, loop/cancellation cases and multilingual/handwriting follow-up. They are not outputs from a running support LLM.

For a bank pilot build a consented, protected, stratified set: product, language/script, document era, scan condition, customer/case permissions, legal clause type, amount/negation questions and adversarial material. Separate training/development from a sealed holdout. Use at least two qualified adjudicators on material legal/financial cases; reconcile disagreements and record label confidence. Balance coverage, not just popularity.

Evaluate the **same held-out queries** against retrieval/prompt/model changes. Report paired per-query deltas, p50/p95 end-to-end and first-safe-token latency, token use, infrastructure cost, safety violations, failure/abstention and quality by stratum. Bootstrap confidence intervals and do a prospective power calculation; an improvement in a handful of English synthetic clauses cannot support bank-wide conclusions. For cost experiments, reject the release if high-risk error or disclosure worsens, even when average judge score improves.

## Make LLM-as-a-judge trustworthy enough to assist

Define a rubric for correctness, citation support, completeness, temporal validity, privacy and escalation. Blind model identity, randomise/reverse answer order, balance lengths, pass authorised evidence and the question, and demand a structured rubric result. Treat judge input as untrusted and keep it outside action authority.

Calibrate against human labels **separately by risk/language**; report agreement, confusion matrix, false acceptance of material errors and drift. Audit disagreements, self-model bias, verbosity bias and position bias. Use an independent model family where possible, but independence does not prove correctness. Store judge model/prompt/version and allow abstention. A judge is neither ground truth nor a sole release gate for legal advice, privacy violations or financial decisions.
