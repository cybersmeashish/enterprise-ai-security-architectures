# Run the reference product

**Stage: implemented local fixture.** Execute commands from the repository root with Python 3.12.

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/python -m tools.validate_governance examples/governance-pack.json
.venv/bin/python -m aiegateway.demo
.venv/bin/python -m unittest discover -s tests -v
```

The demo starts three loopback provider fixtures, admits a freshly signed policy and runs 12 scenarios. Model responses are deterministic strings, not learned-model inference. Credentials and private signing keys are generated for the local run and are not committed.

`policy.example.json` is an unsigned, fixed-clock illustration dated 19 November 2026. It is not loaded as a trusted runtime policy; the demo creates a fresh short-lived policy for your actual local run.

For interactive HTTP use:

```sh
.venv/bin/python -m aiegateway.demo --serve
```

Use the temporary URL and government token printed by your own local process:

```sh
curl "$GATEWAY_URL/v1/generate" \
  -H "Authorization: Bearer $GATEWAY_TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: my-local-request-1' \
  --data-binary @examples/request.json
```

Set the two variables from the values printed locally. The reference server binds only 127.0.0.1. Ctrl-C stops the demo and removes its temporary state. Credentials expire after one hour; this is not enterprise SSO.

For a Docker demonstration, prepare matching Linux wheels while connected:

```sh
.venv/bin/python -m tools.prepare_wheels --architecture amd64
docker pull python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b
docker build --network=none --pull=false -t ashish-enterprise-ai-gateway:0.1.0 .
.venv/bin/python -m tools.run_isolated --output /tmp/gateway-report.json
```

Use `arm64` on an ARM host and `amd64` on x86-64. The wheel directory must be empty before preparation. Build dependency installation is hash-checked with no network; runtime has no external network, runs as UID 65532, uses a read-only root filesystem and drops capabilities.

[API contract](api.md) · [Evidence interpretation](../../../evidence/README.md)
