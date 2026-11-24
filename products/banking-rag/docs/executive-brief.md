# Executive decision brief — a century of bank records, safely searchable

**Decision:** fund a controlled, India-hosted archive-to-evidence programme before committing to a 100M-document monthly service. Start with an internal read-only assistant; retain independent approval for financial, KYC and legal decisions.

**Value to test:** faster document discovery, source-linked support drafting, traceable clause research and visible gaps in the archive. No financial return or client outcome is claimed without a measured baseline.

**Why RAG:** evidence can be permission-filtered, updated and cited without putting customer facts into model weights. Prompting controls interaction; fine-tuning may later improve a narrow task but does not replace versioned, authorised knowledge.

**What can block scale:** physical conservation/capture, missing rights/owners, poor historical OCR, multilingual coverage, review capacity, index/permission reconciliation and inference queues. Count successfully admitted logical documents rather than raw uploads. The calculator separates scans, pages, chunks, storage and inference.

**What to approve now:** archive survey and legal applicability review; a stratified ingestion pilot; read-only identity/knowledge boundary; a protected human-labelled evaluation; supplier/model admission; measurable cost/latency and restoration experiments.

**Risk decisions:** keep originals/derived data/model serving/operators/recovery inside approved boundaries; refuse uncertain evidence; enforce document/customer access outside the LLM; prohibit self-approved tool actions; treat cache and memory as sensitive stores.

**Targets awaiting evidence:** 100M/month admitted documents; 70% lower complete cost per acceptable answer; task-class latency objectives. The repository's learned-model result is a small synthetic ranking experiment, not a bank deployment or answer-quality guarantee.

[Acceptance gates](acceptance-plan.md) · [Full design](enterprise-design.md) · [Execution evidence](../evidence/README.md).
