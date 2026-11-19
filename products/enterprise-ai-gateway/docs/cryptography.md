# Key custody, policy signatures and post-quantum readiness

**Implemented:** maintained `cryptography` Ed25519 verifies the exact policy against a separately supplied public trust anchor. Site, issue/expiry time, schema and revision are checked; the local durable store rejects lower revisions and a changed digest at the same revision. AES-GCM protects cached responses with the scoped key as associated data.

**Trust limitations:** the demo generates its signer and replay key in software. It does not demonstrate HSM custody, independent production approval or signer separation. The SQLite store contains plaintext metadata, budgets and approval hashes; encrypting cached responses does not encrypt the whole database.

| Dependency | Purpose | Current reference | Transition question |
|---|---|---|---|
| Policy artifact signature | Authenticity/integrity | Ed25519, classical | Can a maintained post-quantum signature preserve admission interoperability? |
| Response replay key | Symmetric encryption | AES-GCM, ephemeral 256-bit key | How are custody, rotation, restore and tenant key separation enforced? |
| TLS provider connection | Key establishment and authentication | Not implemented remotely | Which endpoint/identity stacks support the chosen transition? |
| Long-lived evidence | Integrity and archival verification | Unanchored local hash chain | How will checkpoints remain independently verifiable over time? |

Separate key establishment from signatures; a quantum migration inventory does not prove quantum safety. Link to [cryptographic research](https://github.com/cybersmeashish/crypto-implementations) and the measured PQ interoperability work in [disconnected cloud security](https://github.com/cybersmeashish/sovereign-disconnected-cloud-security). No PQ transport, FIPS validation or cryptographic certification is claimed for this gateway.
