# Measured synthetic HTTP cohorts

**Original experiment:** unique, uncached generate requests over real loopback HTTP, deterministic provider fixture and local SQLite. Five warm-up requests excluded. Sixty requests each at concurrency 1, 4 and 8.

These results measure the complete fixture path, including gateway, provider fixture and SQLite I/O. They do not isolate gateway overhead or measure learned-model inference, task quality, billing, large-scale capacity or an enterprise SLO.

| Environment | Concurrency | Success/sample | Successful requests/s | p50 ms | p95 ms | p99 ms |
|---|---|---|---|---|---|---|
| host | 1 | 60/60 | 161.08 | 6.00 | 7.53 | 8.80 |
| host | 4 | 60/60 | 213.69 | 18.18 | 22.76 | 25.77 |
| host | 8 | 60/60 | 203.92 | 36.20 | 54.76 | 57.74 |
| container | 1 | 60/60 | 874.87 | 1.00 | 1.74 | 2.76 |
| container | 4 | 60/60 | 740.85 | 4.35 | 17.10 | 18.58 |
| container | 8 | 60/60 | 945.31 | 7.75 | 13.50 | 14.67 |

Percentiles use linear interpolation across the observed sample. Each cohort is short, has no real-model latency and cannot establish a stable production percentile.

The isolated container used one CPU, 256 MiB RAM, 96 PIDs, non-root UID 65532, no external network and a read-only root filesystem. Temporary files were on bounded tmpfs. The host run used the machine identified in its report. Operating-system CPU counts reflect visible host hardware, not a container's allocated CPU quota.

[Raw host report](../../../evidence/local/host-report.json) · [Raw container report](../../../evidence/local/container-report.json)
