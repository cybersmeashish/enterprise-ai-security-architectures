# 10 — Defend RAG; serve an open model at scale

## Prompting versus fine-tuning versus RAG

**Prompting** defines role, task, output structure and evidence usage, but cannot fit or permission-filter a century of records. **Fine-tuning** can improve style, extraction behaviour or domain task performance when lawful, well-labelled data exists; it is a poor primary store for changing contracts and customer-specific facts because provenance, update, access and deletion are difficult. **RAG** makes evidence selection, document versions, grants and citations explicit. It is the first choice for this archive because the knowledge changes, is auditable and differs by customer/purpose.

RAG is not inherently truthful. OCR, missing evidence, bad chunking, poisoned content and reasoning errors remain. Keep prompting for the interaction contract, RAG for authorised current evidence and consider narrowly scoped fine-tuning later only after the retrieval baseline shows a task-specific behaviour gap. Do not fine-tune around a permissions failure or memorise customer facts. See the original RAG research in the [source guide](12-source-guide.md).

## Open model admission and serving

Choose a model only after testing permitted-use licence, supported language/domain, context size, security, output constraints and workload. Do not infer suitability for Indian banking from an English benchmark. Admit exact model/tokenizer/config hashes, provenance and dependencies; disable unreviewed remote code. Serve within the approved India boundary with authenticated ingress, egress controls and tenant/purpose quotas. Use separate capacity pools for migration/extraction and interactive support.

Continuous batching can improve utilisation but creates queueing and mixed-length effects. Cap admitted context/output tokens and queue age, prioritise bounded interactive work and reject overload predictably. Test throughput **at the required latency and quality**, not peak tokens/second alone. Use prefill/decode separation only when its KV-transfer, network and residency costs are justified.

## KV and prefix cache

Approximate per-token KV bytes: `2 × layers × KV_heads × head_dimension × bytes_per_value`; multiply by retained tokens and concurrent sequences. This differs for grouped-query attention and compression; verify the actual model architecture, allocator/block overhead and runtime. KV memory is separate from model weights, activations and engine reserve. Headroom must be measured before scheduling.

A runtime prefix cache reuses attention state for exact eligible prefixes; it is not a semantic answer cache. Benchmark time-to-first-token benefit and cache eviction. Avoid cross-tenant/purpose sensitive prefix reuse unless a reviewed implementation enforces safe isolation; timing and retention side channels are part of the threat model. Invalidate/segregate on model, adapter and sensitive policy changes. Do not assume a named runtime's default is sufficient.

## Quantization and load tests

Compare FP16/BF16 with supported weight and/or KV quantization on the same task suite and load. Measure numeric/negation/legal errors, language quality, JSON validity, memory, throughput and p95/p99 latency. A smaller footprint does not guarantee faster kernels or acceptable reasoning. Pick hardware and runtime from actual support and measured results; no GPU count is claimed in this repository.

Run closed-loop user load and open-loop arrival tests to expose saturation; record cancellation and retry amplification, autoscaling cold-start, node loss, model reload and rollback. Publish hardware, engine/model versions, workload distribution, context/output lengths, achieved concurrency, latency and total cost. The only learned-model run in this package is a small CPU retrieval/reranking experiment, not open-LLM serving.
