# Measured synthetic HTTP cohorts

**Original experiment:** unique, uncached generate requests over real loopback HTTP, deterministic provider fixture and local SQLite. Five warm-up requests excluded. Sixty requests each at concurrency 1, 4 and 8.

These results measure the complete fixture path, including gateway, provider fixture and SQLite I/O. They do not isolate gateway overhead or measure learned-model inference, task quality, billing, large-scale capacity or an enterprise SLO.

| Environment | Concurrency | Success/sample | Successful requests/s | p50 ms | p95 ms | p99 ms |
|---|---|---|---|---|---|---|
| host | 1 | 60/60 | 83.94 | 11.39 | 20.30 | 25.22 |
| host | 4 | 60/60 | 101.76 | 36.12 | 72.54 | 90.21 |
| host | 8 | 60/60 | 121.73 | 65.35 | 89.18 | 92.02 |
| container | 1 | 60/60 | 768.56 | 1.18 | 1.73 | 2.96 |
| container | 4 | 60/60 | 685.88 | 5.35 | 11.49 | 12.41 |
| container | 8 | 60/60 | 562.33 | 10.73 | 31.17 | 38.37 |

Percentiles use linear interpolation across the observed sample. Each cohort is short, has no real-model latency and cannot establish a stable production percentile.

The isolated container used one CPU, 256 MiB RAM, 96 PIDs, non-root UID 65532, no external network and a read-only root filesystem. Temporary files were on bounded tmpfs. The host run used the machine identified in its report. Operating-system CPU counts reflect visible host hardware, not a container's allocated CPU quota.

[Raw host report](../../../evidence/local/host-report.json) · [Raw container report](../../../evidence/local/container-report.json)
