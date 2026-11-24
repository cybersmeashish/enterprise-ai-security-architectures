# Enterprise AI Security development

All development, edits, dependency installation, research analysis, execution, tests and artifact generation run inside OrbStack. Use `docker --context orbstack` explicitly. The canonical repository is `enterprise-ai-security-dev:/workspaces/enterprise-ai-security-architectures/repo` with persistent volume `enterprise-ai-security-workspace`. The host copy is for review, transfers and guarded publication only.

Never mount credentials, a home directory or the Docker socket. Preserve the named volume. Restore unavailable OrbStack access or report it rather than falling back to macOS. Preserve account/repository checks, source hashes, non-forced branch updates and remote byte verification.

Follow [Banking RAG instructions](products/banking-rag/AGENTS.md) for the new design and experiment. Preserve the released gateway source/evidence when working on another product. Synthetic experiments must not become production throughput, bank outcome, compliance or quality claims.
