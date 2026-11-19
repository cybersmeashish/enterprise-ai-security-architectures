# Retrieval and knowledge security

**Implemented:** a document ID resolves through a server-side synthetic register. Tenant and subject ACL checks happen before context assembly and before cached replay. Retrieved classification can raise the route's minimum class. The retrieved-context marker is informational, not a prompt-injection security boundary.

**Production contract:** enforce source-system entitlements at ingestion and retrieval; namespace vectors by tenant and purpose; preserve document owner, origin, version, hash, ACL and expiry; quarantine untrusted ingestion; reconcile permission changes and deletion; verify citations against the actual source.

Test poisoning, forged document identifiers, cross-tenant similarity matches, stale ACLs, revoked source access, indirect injection, citation fabrication and retrieval availability. Embedding similarity does not authorize disclosure.

This release has no vector database, embeddings, ingestion jobs or trained model. The test demonstrates that malicious retrieved instructions cannot grant tool authority; it does not prove that an LLM will ignore them or produce a grounded answer.
