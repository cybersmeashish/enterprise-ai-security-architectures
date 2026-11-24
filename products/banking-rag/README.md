# Banking Archive RAG — India enterprise design

**Turn a century of banking records into permission-aware, source-linked answers.**

By Ashish Srivastava · Enterprise AI security, vCISO advisory and governance engineering.

**Stage: design reference plus a bounded synthetic retrieval experiment and executable planning/guardrail tests.** The requested **100 million documents per month**, **70% cost reduction** and low first-token latency are targets to validate, not achieved production results. No bank documents or customer data are used.

[Read the complete enterprise design](docs/enterprise-design.md) · [Executive brief](docs/executive-brief.md) · [Decisions](decisions/README.md) · [Measured evidence](evidence/README.md)

| Question | Design and evidence |
|---|---|
| Can the archive enter RAG at 100M documents/month? | [Physical capture, ingestion and capacity](docs/03-ingestion-capacity.md) |
| How do legal contracts become reliable evidence? | [Clause-aware chunking and search](docs/04-chunking-retrieval.md) |
| How are AI security, governance and RAG security decided? | [Threat model](docs/05-security.md), [India applicability](docs/06-governance-india.md), [decision records](decisions/README.md) |
| How do we find and reduce wrong answers? | [Debugging, evaluation and judge calibration](docs/07-quality-evaluation.md) |
| How might cost fall by 70% while quality stays acceptable? | [Cache, routing, latency and experiment gates](docs/08-cost-latency.md) |
| How do agents, memory, JSON and injection boundaries work? | [Agent design](docs/09-agents-memory-json.md) |
| How is an open model served and changed safely? | [Serving](docs/10-serving.md), [SSE, tracing and rollback](docs/11-operations.md) |

[All 25 requested capabilities](docs/request-coverage.md) · [Primary-source reading guide](docs/12-source-guide.md) · [Lab instructions](lab/README.md) · [Next measured work](docs/acceptance-plan.md)

## Connect to the wider portfolio

Use the [Enterprise AI Gateway](../enterprise-ai-gateway/README.md) as a policy-boundary reference; this design does not pretend its synthetic adapter is a production bank connector. Link sector decisions to [BFSI](https://github.com/cybersmeashish/bfsi-security), [sovereign/disconnected cloud](https://github.com/cybersmeashish/sovereign-disconnected-cloud-security), [Sovereign AI](https://github.com/cybersmeashish/sovereign-AI), and [Modern SOC Design](https://github.com/cybersmeashish/modern-soc-design).
