# Product execution evidence

| Evidence | What it establishes |
|---|---|
| [Host report](local/host-report.json) and [test log](local/host-tests.log) | 92 unique tests, 12 scenarios, real loopback HTTP cohorts and local snapshot checks |
| [Isolated container report](local/container-report.json) and [test log](local/container-tests.log) | Same input hashes and tests; UID 65532, loopback-only interfaces, unreachable external-connect probe and constrained container |
| [CI status](ci-verification.md) | GitHub run, tested commit and retained artifact status; updated after actual execution |

Reports include source SHA-256, environment, successful/error counts, latency distributions, restoration scope and known gaps. The same 92 tests executed in multiple environments are **92 unique tests**, not an inflated count.

There are 12 separate operational scenarios, followed by 180 measured requests in three short cohorts. Model task quality is unmeasured. The report distinguishes logical/synthetic regions from actual network isolation.

Source manifests cover runtime code, tools, tests, examples, the lockfile and Dockerfile. Documentation/evidence-only changes do not change those implementation hashes. A source manifest establishes correspondence, not software trust or complete provenance.

Local restore checks cover a SQLite consistent snapshot, budget and audit chain. Identity, provider authority, KMS and independent checkpoints are outside that recovery proof.
