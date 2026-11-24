# 01 — Mission, scope and boundaries

The bank wants to search historical contracts, receipts, vouchers, correspondence and physical records, then answer staff questions with inspectable evidence. It has records dating back approximately a century. Age does not establish authenticity, retention authority or present-day applicability.

The first release is an **internal, read-only research and customer-support drafting assistant**. It may locate a receipt, explain a cited contract clause or draft an answer for a trained employee. It cannot approve loans, move money, alter KYC, give a final legal interpretation or substitute a historical tariff for the current authoritative policy. Consequential decisions stay in existing bank workflows with independent authority and human review.

### Assumptions that must be accepted

- The reference assumes an India-regulated scheduled commercial bank. The actual legal entity, subsidiaries, bank class and outsourcing arrangements must be confirmed; not every RBI direction has the same applicability.
- Originals, OCR, embeddings, indexes, prompts, inference, logs, backups and administration are proposed to remain in bank-approved Indian locations. This is a design boundary pending legal and procurement acceptance, not a blanket assertion that every bank dataset has the same statutory localisation rule.
- 100M means **successfully admitted logical documents per 30-day planning month**, not uploaded files, attempts, pages or chunks. The bank must agree how multipage bundles, duplicate scans and amendments are counted.
- The first scenario uses six pages per document, 450 tokens per page, eight searchable chunks per document and 5% processing amplification. These are synthetic assumptions, not an archive survey.
- Interactive workload is separate: a proposed 100 requests/second sustained and 300 peak. The actual concurrent users, languages and case mix require measurement.
- Retention is per record class, legal hold and approved purpose. A 100-year archive is not a 100-year retention instruction for every derived index or chat.

### Intended users and harm

Records staff need provenance and capture progress. Legal teams need clause context, amendments and uncertain OCR explicitly visible. Customer-support employees need current product rules without exposing other customers. Audit teams need reconstructable decisions. Security and privacy teams need boundary evidence and revocation tests. Leadership needs cost per successfully admitted document and per acceptable answer, not a count of generated tokens.

Release in stages: inventory and preservation; controlled ingestion; read-only retrieval; grounded answer drafting; bounded tools. Broader autonomy is a separate approval. No real bank data, customer result, production throughput, operational quality or regulatory certification is asserted by this repository.

**Read next:** [architecture](02-architecture.md), [capacity](03-ingestion-capacity.md), [India applicability](06-governance-india.md).
