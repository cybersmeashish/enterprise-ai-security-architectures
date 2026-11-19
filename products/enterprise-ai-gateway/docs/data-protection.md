# Data handling and privacy

**Implemented:** the effective class is the highest of the use-case floor, caller-declared higher class and retrieved-document class. Approved model metadata must allow that class and region. Telemetry excludes prompt, response and bearer content. Idempotency responses are AES-GCM encrypted and bound to their scoped request key.

**Bounded fixture:** ASCII email and `DEMO_SECRET_` checks exercise input/output rejection. They are not a DLP product. An obfuscated email is intentionally accepted in a regression test to expose the limitation.

**Design obligations:** inventory data subject, purpose, collection source, lawful/contractual authority, provider processing/retention, support access, transfer, backups and deletion. Audit identifiers remain potentially sensitive. Encrypt the underlying store and backups, separate keys from backups, and implement accountable access and deletion.

Replay TTL is 30 seconds, enforced logically; deletion happens opportunistically on a later claim. Expiry does not establish physical erasure of SQLite pages or backup copies. The default replay key is ephemeral, so restart without a separately retained key prevents replay rather than silently regenerating a response.

No personal data is supplied in the public examples. No privacy law compliance is established by this toolkit.
