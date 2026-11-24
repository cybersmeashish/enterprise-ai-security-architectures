# 06 — Dedicated AI governance and India applicability

**Governance decision:** a named bank use-case owner accepts the permitted purpose, benefit, users, dataset scope, risk tier and stop conditions. Model-risk, information security, privacy/legal, records, outsourcing and operations owners review their own evidence. Internal audit retains independent assurance. A vendor's model card or a passing lab does not replace bank accountability.

## India reference and verification status

The source guide records the official RBI **Master Direction on Information Technology Governance, Risk, Controls and Assurance Practices** (7 November 2023) and **Master Direction on Outsourcing of Information Technology Services** (10 April 2023), retrieved for this design. Their applicability depends on regulated entity type and the current directions/amendments. The governance direction informs oversight, segregation, risk/control assurance, changes and continuity. The outsourcing direction informs retained accountability, due diligence, agreements, access/audit rights, concentration and exit.

The Digital Personal Data Protection Act, associated rules and commencement notifications require a **current legal applicability and commencement check**. Do not treat publication of a rule as proof that every section is already in force. The source register distinguishes accessible primary text from unavailable pages; unresolved commencement/amendment items block a compliance sign-off. CERT-In obligations and payment-system data-storage directions are separate applicability questions. The payment-specific rule must not be represented as an automatic blanket rule for all historical bank documents.

India-hosted processing in this reference is a proposed bank policy and risk boundary covering originals, derivatives, vector indexes, model serving, operators, logs, backups and recovery. The bank must identify any cross-border support, telemetry or subprocessor route even if the primary compute region is Indian. Define key custody, support approval, export recipients and incident evidence boundaries explicitly.

## Governance evidence pack

Maintain a versioned use-case card, system/data flow, dataset custody and rights inventory, model/prompt/embedding cards, approved purpose/fields, risk register, security tests, evaluation report, language/era limitations, supplier contract assessment, incident/rollback playbook, retention schedule and acceptance record. Every “control” maps to an owner and actual evidence or an unresolved gap.

Track data provenance and permitted use for digitisation, indexing, support, legal review and model training separately. The default prohibits training/fine-tuning on bank material. Historical availability does not imply consent, purpose compatibility or ownership. Legal holds and preservation may coexist with restricted derived access; resolve deletion/retention conflicts through approved record-specific decisions.

## Decision rights and changes

- Business owner: usefulness, scope, budget and high-risk escalation.
- Records/data owner: custody, indexing permission, authenticity status, retention and version precedence.
- Legal/privacy: basis, applicable duties, historical records, notices, restricted fields, cross-border and contractual constraints.
- CISO/security: identity, grants, supplier/model admission, injection/exfiltration tests and incident response.
- Model-risk/AI governance: validated languages, task limits, answer quality, judge calibration and change acceptance.
- Platform/SRE: service objectives, capacity, monitoring, restoration and release/rollback execution.
- Independent assurance: sample selection, unresolved findings and evidence reproducibility.

A model, prompt, OCR, embedding, chunker, reranker, policy, cache, tool or corpus change is an independently versioned release surface. Approved changes undergo paired evaluation and boundary tests. Emergency suspension can disable generation while preserving authorised search. “No answer” and “human review required” are governed outcomes, not failure metrics to hide.

Use the [risk register](../templates/risk-register.csv), [applicability worksheet](../templates/india-applicability.csv) and [acceptance plan](acceptance-plan.md). This is a traceable design aid, not a legal determination or RBI certification.
