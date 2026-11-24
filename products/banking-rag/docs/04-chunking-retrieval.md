# 04 — Legal chunking, BM25, dense, hybrid and reranking

## Decision: clause-aware parent/child chunks

For legal contracts, preserve the title, parties as approved surrogates, agreement/version ID, clause path, definitions, schedule/table links and effective date. Parse layout before chunking. The initial design uses **450–700 model tokens per child clause**, at most approximately **10–15% overlap within an oversized clause**, and a **1,500–2,500 token parent section** expanded only after permission checks. These starting values require evaluation using the chosen tokenizer; they are not universal best sizes.

Do not split a short clause just to meet a target. If a clause is oversized, split at subclauses/sentences, repeat the heading and preserve child offsets. Do not overlap across customer, agreement or grant boundaries. Keep definitions, exclusions, amendments and cross-references as explicit relations; retrieving a termination right without its notice exception is incomplete evidence. Store page/box coordinates so the analyst can inspect the original. Preserve a table header with the relevant row, units and footnotes. Do not turn merged cells into unaudited prose.

The toy lab chunker demonstrates layout-record boundaries and provenance using whitespace tokens. It is not a production legal parser or exact model-token chunker. [Microsoft's chunking guide](12-source-guide.md) supplies primary implementation context, not a validation of these parameters.

## When to use each retrieval method

| Method | Prefer when | Failure to test |
|---|---|---|
| BM25 | Exact receipt IDs, contract clause numbers, rare terms, product codes and legal wording | OCR substitutions, inflection, transliteration and paraphrases |
| Dense vectors | Natural-language paraphrases and conceptual similarity in a validated language/domain | Numbers/negation, rare codes, out-of-domain wording, unsupported language and semantic near-misses |
| Hybrid | The mixed archive and general support questions | Added cost, correlated failures, poor score fusion and weak filters |

Use hybrid as the general default; route an exact structured-ID lookup to an authorised deterministic index before semantic search. Apply the same trusted filters to both sparse and dense retrieval. Union the authorised candidates, fuse by reciprocal rank (`sum 1/(60+rank)` as an initial parameter), deduplicate by document version/clause and retain ranking provenance. Do not add incomparable raw BM25 and cosine scores without calibration. Start with top 50 per search path, rerank a bounded union and send approximately 4–8 sufficient clauses to generation; tune on latency and evidence recall, not model preference.

## Add the reranker and test the trade-off

A cross-encoder evaluates the query/candidate pair more closely than independent embeddings. Its score is not calibrated answer confidence. Include required clause context, effective date and a truncation flag; an unobserved exception beyond the input window can invalidate its rank. Rerank only authorised candidates and never use its ranking to override policy.

The lab uses real downloaded ONNX embedding and cross-encoder models, exact artifact hashes, English synthetic clauses and explicit synthetic relevance labels. It compares **BM25**, **dense**, **hybrid RRF** and **hybrid plus cross-encoder reranking** on the same queries. The [measured results](../evidence/retrieval-results.json) and [per-query rows](../evidence/retrieval-per-query.csv) report MRR@10, Recall@5, nDCG@3 and timing. Results may show a regression; they must not be tuned and relabelled to force improvement.

This small benchmark tests ranking only. It does not measure a real bank archive, Indian-language retrieval, human answer correctness or production latency. A bank release needs sealed holdouts, customer isolation, OCR strata, temporal contradictions and a representative model. Add reranking only when paired quality gains justify its tail latency and cost, or scope it to difficult queries.
