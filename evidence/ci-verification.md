# Hosted product verification

**Passed:** [GitHub run 44458045970](https://github.com/cybersmeashish/enterprise-ai-security-architectures/actions/runs/44458045970) for implementation commit
[`8db8ca775d5c`](https://github.com/cybersmeashish/enterprise-ai-security-architectures/commit/8db8ca775d5c969f2899365528485e8c542b56b1).

- 92 unique regression tests passed; 12 operational scenarios passed.
- The actual hosted artifact has the same 27 selected source hashes as the current runtime.
- Container execution was non-root UID 65532, loopback-only, with an unreachable external-connect probe.
- Three synthetic HTTP cohorts each completed 60 requests at concurrency 1, 4 and 8.

[Unmodified artifact report](github/gateway-report.json) · [Retained test log](github/gateway-tests.log) · [Inspection record](github/verification.json)

The hosted workflow installed hash-locked dependencies, validated governance records, ran the native suite,
built without networking and ran the isolated suite. Passing the same tests in multiple environments does not
increase the count of unique tests. Hosted artifacts are retained for 14 days; the copies above preserve this
run's report in the repository history.

Evidence/documentation-only follow-up commits have the same selected implementation inputs. Synthetic providers,
declared regions and short HTTP cohorts do not establish learned-model quality, actual cloud residency or
large-scale enterprise capacity.
