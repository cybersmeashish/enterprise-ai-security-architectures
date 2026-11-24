# Banking RAG development rules

All development, research analysis, edits, installs, execution, tests and artifact generation run inside OrbStack. Use `docker --context orbstack` explicitly.

Canonical container: `enterprise-ai-security-dev`. Workspace: `/workspaces/enterprise-ai-security-architectures/repo`. Persistent volume: `enterprise-ai-security-workspace`. Model artifacts, wheels and runtime live in `/workspaces/enterprise-ai-security-architectures/work` and `/workspaces/enterprise-ai-security-architectures/runtime`, outside public source.

The host copy is for review, transfers and guarded publishing only. Never mount credentials, the home directory or Docker socket. Preserve the named volume. Restore OrbStack or report inability rather than falling back to host runtimes. Publish only after account/branch checks, reviewed-source manifest checks, non-forced updates and remote byte verification.

Use synthetic data. Distinguish calculations, static guardrail tests and actual learned ranking experiments from production banking throughput, answer quality, privacy, compliance and financial outcomes. Update evidence after source changes. Never claim cost/latency targets achieved from assumed prices or timing a small retrieval lab.
