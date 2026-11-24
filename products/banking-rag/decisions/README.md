# Banking RAG architecture decisions

All decisions are adopted **for this reference design**. Production implementation and bank acceptance remain pending. Local lab checks cover only their stated subsets.

| ID | Decision | Accountable owners |
|---|---|---|
| 0001 | [India-controlled data plane](0001-india-controlled-data-plane.md) | Platform, legal and CISO |
| 0002 | [AI security and independent authority](0002-ai-security-and-independent-authority.md) | CISO and service owners |
| 0003 | [AI governance and bank accountability](0003-ai-governance-and-bank-accountability.md) | Business, AI governance, legal and risk |
| 0004 | [RAG security and document permissions](0004-rag-security-and-document-permissions.md) | Data owner and identity service |
| 0005 | [Clause-aware legal chunking](0005-clause-aware-legal-chunking.md) | Records/legal and retrieval lead |
| 0006 | [Hybrid retrieval with measured reranking](0006-hybrid-retrieval-with-measured-reranking.md) | Retrieval lead and model-risk |
| 0007 | [PII before embedding rerank and inference](0007-pii-before-embedding-rerank-and-inference.md) | Privacy, records and model-risk |
| 0008 | [70 percent cost target with quality gates](0008-70-cost-target-with-quality-gates.md) | Business, FinOps and model-risk |
| 0009 | [Semantic cache with scoped reuse](0009-semantic-cache-with-scoped-reuse.md) | Security, retrieval and SRE |
| 0010 | [Risk-based cheap and smart routing](0010-risk-based-cheap-and-smart-routing.md) | Model-risk and business owner |
| 0011 | [Bounded tools and loop termination](0011-bounded-tools-and-loop-termination.md) | Application/service owners and CISO |
| 0012 | [Long-running memory is evidence not policy](0012-long-running-memory-is-evidence-not-policy.md) | Privacy, identity and application owner |
| 0013 | [Schema-valid application JSON](0013-schema-valid-application-json.md) | Application owner and security |
| 0014 | [RAG before archive fine-tuning](0014-rag-before-archive-fine-tuning.md) | Records, privacy and model-risk |
| 0015 | [Open-model batching KV and quantization](0015-open-model-batching-kv-and-quantization.md) | Platform and model-risk |
| 0016 | [SSE safe output and disconnects](0016-sse-safe-output-and-disconnects.md) | Application and SRE |
| 0017 | [Trace each agent without raw PII](0017-trace-each-agent-without-raw-pii.md) | Platform, security and privacy |
| 0018 | [Compatible prompt rollback](0018-compatible-prompt-rollback.md) | Release owner, model-risk and incident owner |
