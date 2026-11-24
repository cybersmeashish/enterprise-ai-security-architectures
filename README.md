# Enterprise AI Security Architectures

[![Verify Enterprise AI Gateway](https://github.com/cybersmeashish/enterprise-ai-security-architectures/actions/workflows/verify.yml/badge.svg)](https://github.com/cybersmeashish/enterprise-ai-security-architectures/actions/workflows/verify.yml)

**Security and governance engineering for enterprise AI, from the request boundary to the operating model.**

By [Ashish Srivastava](https://github.com/cybersmeashish) · First product: **Enterprise AI Gateway v0.1.0**

This portfolio connects application security, AI security, cloud architecture, sovereign operation and governance evidence. Each product must explain its decisions, publish inspectable artifacts, exercise denied cases and report unresolved risks.

| Product | What you can inspect today | Stage |
|---|---|---|
| [Enterprise AI Gateway](products/enterprise-ai-gateway/README.md) | Runnable HTTP reference, policy admission, tenant boundaries, controlled synthetic tools, governance pack and measured experiments | Security reference preview v0.1.0 |
| [Banking Archive RAG — India](products/banking-rag/README.md) | 100M/month archive ingestion design, legal chunking, AI/RAG security, governance, bounded planning/guardrail tools and a measured synthetic learned-reranker experiment | Enterprise design reference; production acceptance pending |

Start with the [product guide](products/enterprise-ai-gateway/README.md), [five-minute demo](products/enterprise-ai-gateway/docs/quickstart.md), [security coverage](products/enterprise-ai-gateway/docs/coverage.md), or [executive decision brief](products/enterprise-ai-gateway/docs/executive-brief.md).

The product website is published from [`docs/`](docs/index.html). [Releases](https://github.com/cybersmeashish/enterprise-ai-security-architectures/releases) record versioned capabilities and limits. [Verification runs](https://github.com/cybersmeashish/enterprise-ai-security-architectures/actions/workflows/verify.yml) retain measured execution evidence.

## Portfolio connections

- [Sovereign AI & Security](https://github.com/cybersmeashish/sovereign-AI): local model, retrieval and tool authority.
- [Sovereign & disconnected cloud security](https://github.com/cybersmeashish/sovereign-disconnected-cloud-security): connectivity, import, key custody and recovery controls.
- [Government security](https://github.com/cybersmeashish/government-security): public-service ownership, assurance and human authority.
- [Research](https://github.com/cybersmeashish/Ashish-research): source-led notes and experimental questions.

## Evidence over feature lists

**Implemented** means exercised code in this repository. **Design** means a documented architecture or control contract. **Roadmap** means work still to be built. The gateway's synthetic providers exercise security and failure boundaries. Banking Archive RAG adds a small learned-encoder ranking experiment, scoped to synthetic English clauses; neither establishes real bank answer quality or enterprise inference capacity.

Future products enter the [architecture portfolio](products/README.md) after they have a specific problem, owner, threat model, repeatable example and evidence. No empty product repositories or implied deployments are needed.
