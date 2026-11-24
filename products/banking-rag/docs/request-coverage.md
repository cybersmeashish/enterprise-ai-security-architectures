# Requested capability coverage

The user's repeated numbering is normalised into 25 capability groups. Design, executed lab and production evidence are kept distinct.

| ID | Capability | Design | Current evidence |
|---|---|---|
| R01 | Archive 100M/month | [03-ingestion-capacity.md](03-ingestion-capacity.md) | Executable assumption-based calculator; no actual 100M ingest |
| R02 | AI security | [05-security.md](05-security.md) | Design; intended-environment acceptance pending |
| R03 | AI governance | [06-governance-india.md](06-governance-india.md) | Design; intended-environment acceptance pending |
| R04 | RAG security | [05-security.md](05-security.md) | Design; intended-environment acceptance pending |
| R05 | Wrong-answer debugging | [07-quality-evaluation.md](07-quality-evaluation.md) | Design; intended-environment acceptance pending |
| R06 | Legal contract chunking | [04-chunking-retrieval.md](04-chunking-retrieval.md) | Design; intended-environment acceptance pending |
| R07 | BM25 dense and hybrid | [04-chunking-retrieval.md](04-chunking-retrieval.md) | Design; intended-environment acceptance pending |
| R08 | Measured reranker | [04-chunking-retrieval.md](04-chunking-retrieval.md) | Actual learned-encoder ranking experiment on synthetic English texts |
| R09 | 70% cost reduction target | [08-cost-latency.md](08-cost-latency.md) | Hypothetical cost calculation; quality/cost target not demonstrated |
| R10 | First-safe-token latency | [08-cost-latency.md](08-cost-latency.md) | Design; intended-environment acceptance pending |
| R11 | Semantic cache and hit rate | [08-cost-latency.md](08-cost-latency.md) | Bounded synthetic lab checks; production controls pending |
| R12 | Cheap versus smart routing | [08-cost-latency.md](08-cost-latency.md) | Bounded synthetic lab checks; production controls pending |
| R13 | Reliable tool agent | [09-agents-memory-json.md](09-agents-memory-json.md) | Bounded synthetic lab checks; production controls pending |
| R14 | Agent loop repair | [09-agents-memory-json.md](09-agents-memory-json.md) | Bounded synthetic lab checks; production controls pending |
| R15 | Long-running memory | [09-agents-memory-json.md](09-agents-memory-json.md) | Design; intended-environment acceptance pending |
| R16 | Schema-valid JSON | [09-agents-memory-json.md](09-agents-memory-json.md) | Bounded synthetic lab checks; production controls pending |
| R17 | Hallucination detection and reduction | [07-quality-evaluation.md](07-quality-evaluation.md) | Design; intended-environment acceptance pending |
| R18 | Support bot eval suite | [07-quality-evaluation.md](07-quality-evaluation.md) | Design; intended-environment acceptance pending |
| R19 | Trustworthy judge calibration | [07-quality-evaluation.md](07-quality-evaluation.md) | Design; intended-environment acceptance pending |
| R20 | Tool-agent prompt injection | [05-security.md](05-security.md) | Design; intended-environment acceptance pending |
| R21 | PII before model paths | [05-security.md](05-security.md) | Bounded synthetic lab checks; production controls pending |
| R22 | Fine-tune RAG prompting decision | [10-serving.md](10-serving.md) | Design; intended-environment acceptance pending |
| R23 | Open model batching KV quantization | [10-serving.md](10-serving.md) | Design; intended-environment acceptance pending |
| R24 | SSE and disconnects | [11-operations.md](11-operations.md) | Design; intended-environment acceptance pending |
| R25 | Multi-agent trace and prompt rollback | [11-operations.md](11-operations.md) | Design; intended-environment acceptance pending |
