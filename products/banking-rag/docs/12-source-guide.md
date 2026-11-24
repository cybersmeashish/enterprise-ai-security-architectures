# Primary-source reading guide

**Reviewed for this draft on 24 November 2026.** Sources explain standards, research or implementation context; they do not endorse this design or demonstrate bank deployment. The original architecture and proposed thresholds are explicitly separate from source facts.

Start with RBI governance/outsourcing for applicability, NIST/OWASP for risk, the chunking/hybrid guides for retrieval, and the RAG/judge papers for evaluation limits.

| ID | Primary reference | Use in this design | Status |
|---|---|---|
| nist-genai | [NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | Risk assessment, evaluation and lifecycle governance | retrieved_reference |
| rbi-it-governance | [RBI IT governance direction, 2023](https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12562&Mode=0) | Bank entity applicability, governance, controls, assurance and continuity | retrieved_reference |
| rbi-it-outsourcing | [RBI IT outsourcing direction, 2023](https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12486&Mode=0) | Retained accountability, supplier oversight, audit/access, concentration and exit | retrieved_reference |
| meity-data-protection | [Unresolved reference target](https://www.meity.gov.in/data-protection-framework) | Not used for specific legal/provider claims | unresolved_or_non_substantive |
| ms-chunking | [Microsoft AI Search chunking guide](https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents) | Structural/size trade-offs; initial parameters here remain design hypotheses | retrieved_reference |
| ms-hybrid | [Microsoft hybrid search overview](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview) | Sparse and vector retrieval with rank fusion | retrieved_reference |
| ms-reranker | [Microsoft semantic ranking overview](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview) | Secondary ranking trade-offs; not the local reranker implementation | retrieved_reference |
| ms-document-access | [Microsoft document-level access overview](https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview) | Access-control integration considerations; capability/preview checks required | retrieved_reference |
| owasp-genai | [OWASP GenAI risk taxonomy](https://genai.owasp.org/llm-top-10/) | Prompt injection, disclosure, agency and related threat coverage | retrieved_reference |
| vllm-prefix | [vLLM automatic prefix caching](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/) | Runtime prefix reuse, distinct from semantic answer caching | retrieved_reference |
| vllm-quantization | [vLLM quantization reference](https://docs.vllm.ai/en/latest/features/quantization/) | Engine/hardware/model support requires verification and measurement | retrieved_reference |
| openai-json | [Unresolved reference target](https://developers.openai.com/api/docs/guides/structured-outputs) | Not used for specific legal/provider claims | unresolved_or_non_substantive |
| openai-latency | [Unresolved reference target](https://developers.openai.com/api/docs/guides/latency-optimization) | Not used for specific legal/provider claims | unresolved_or_non_substantive |
| whatwg-sse | [WHATWG server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html) | Event format, reconnect and browser behaviour | retrieved_reference |
| presidio | [Unresolved reference target](https://microsoft.github.io/presidio/) | Not used for specific legal/provider claims | unresolved_or_non_substantive |
| sbert-crossencoder | [Sentence Transformers cross-encoder guide](https://sbert.net/docs/cross_encoder/usage/usage.html) | Query/passage pair ranking implementation context | retrieved_reference |
| model-reranker | [ms-marco-MiniLM-L6-v2 model repository](https://huggingface.co/api/models/cross-encoder/ms-marco-MiniLM-L6-v2) | Exact cross-encoder revision/artifact provenance for the English lab | retrieved_reference |
| model-embedding | [all-MiniLM-L6-v2 model repository](https://huggingface.co/api/models/sentence-transformers/all-MiniLM-L6-v2) | Exact model revision/artifact provenance for the English lab | retrieved_reference |
| otel-genai | [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) | Versioned model/workflow observability; check convention stability | retrieved_reference |
| rag-paper | [Original RAG research paper](https://arxiv.org/abs/2005.11401) | Retrieval-augmented knowledge architecture research | retrieved_reference |
| judge-paper | [LLM judge evaluation research](https://arxiv.org/abs/2306.05685) | Bias/limitations informing calibration and human adjudication | retrieved_reference |
| cert-in | [CERT-In directions under section 70B, 2022](https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf) | Separate incident/log obligation applicability check | retrieved_reference |
| dpdp-act | [Unresolved reference target](https://www.indiacode.nic.in/bitstream/123456789/20064/1/a2023-22.pdf) | Not used for specific legal/provider claims | unresolved_or_non_substantive |
| rbi-payment-storage | [RBI payment-system data storage, 2018](https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=11244&Mode=0) | Payment-specific boundary; do not generalise to every bank document | retrieved_reference |
| presidio-new | [Presidio project documentation](https://data-privacy-stack.github.io/presidio/) | Detection/redaction patterns; no complete PII-detection guarantee | retrieved_reference |
| meity-rules-2025 | [Unresolved reference target](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?pageTitle=Digital-Personal-Data-Protection-Rules-2025) | Not used for specific legal/provider claims | unresolved_or_non_substantive |

## Legal status and unresolved material

The official RBI direction bodies and payment-storage page were inspected, and the CERT-In PDF was retrieved. The latest bank-entity scope, amendments, other binding instruments and actual contractual duties require legal/compliance acceptance. The MeitY Rules-2025 landing route returned a client-rendered shell; full current DPDP rules/commencement text was not verified in this run. The India Code Act download also failed. No date-specific assertion that all DPDP provisions are in force is made. These unresolved primary/legal checks remain explicit blockers to a compliance sign-off.

## Retrieval models and attribution

The experiment loads Sentence Transformers `all-MiniLM-L6-v2` and `cross-encoder/ms-marco-MiniLM-L6-v2` from exact repository revisions. Both repository metadata declare Apache-2.0. Consult the original model cards and upstream licence terms. Weights/tokenizers are cached outside public source and are not redistributed in this contribution. [Model hashes](../evidence/model-manifest.json) record the exact tested artifacts. This experiment does not establish multilingual Indian banking suitability.

## Reproducibility and limits

[Source register](../fixtures/source-register.json) retains requested/resolved URLs, retrieval time, HTTP/error status and source hashes. A hash proves the recorded bytes, not the authority of a source or unchanged future content. Raw third-party pages/PDFs stay outside the public source. No unavailable target is used to substantiate a specific claim.

The retrieved vLLM `latest` pages identify themselves as developer-preview documentation. Pin the intended stable engine release and its matching documentation before selecting production features. No engine feature is treated as measured here.
