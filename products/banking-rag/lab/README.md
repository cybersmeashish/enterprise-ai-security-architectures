# Reproduce the bounded banking RAG lab

Use the persistent OrbStack repository workspace in [AGENTS.md](../AGENTS.md). Development, setup and execution stay in that container; no host runtime is required. Work files, downloaded models and wheels stay outside public source.

## What runs

- `core.py`: editable document/page/capture/worker/storage and hypothetical generation-cost calculations; structured clause chunks; synthetic grant checks; scoped in-memory semantic-cache boundary/counters; trusted routing flags; bounded tool-plan loop checks; schema/error envelopes.
- `verify.py`: meaningful regression tests, fixture/spec checks, planning outputs, source hashes, links and optional real learned-model ranking.
- `retrieval_benchmark.py`: real local ONNX embeddings/cross-encoder, BM25 and RRF on 24 synthetic English texts and 18 queries. It does not call an answering LLM.

## Standard-library checks inside OrbStack

```sh
docker --context orbstack exec enterprise-ai-security-dev python products/banking-rag/lab/verify.py --output /workspaces/enterprise-ai-security-architectures/work/core-check
```

## Exact optional ranking environment

The checked environment uses Linux aarch64/Python 3.12. `requirements-aarch64.lock` contains exact wheel hashes for the tested environment, including research/PDF extraction dependencies. `requirements.txt` pins the direct ranking packages; it is not the full supply-chain lock. Other platforms need separately prepared/verified wheels and evidence.

Inside the development container, create a persistent virtual environment outside source. Download the hash-locked wheels during controlled setup, then install from the local wheel directory with networking disabled where possible. Do not mix this optional ranking environment with the gateway's existing release lock.

```sh
docker --context orbstack exec enterprise-ai-security-dev python -m venv /workspaces/enterprise-ai-security-architectures/runtime
docker --context orbstack exec enterprise-ai-security-dev /workspaces/enterprise-ai-security-architectures/runtime/bin/python -m pip download --require-hashes -r products/banking-rag/lab/requirements-aarch64.lock -d /workspaces/enterprise-ai-security-architectures/work/wheels
docker --context orbstack exec enterprise-ai-security-dev /workspaces/enterprise-ai-security-architectures/runtime/bin/python -m pip install --no-index --find-links /workspaces/enterprise-ai-security-architectures/work/wheels --require-hashes -r products/banking-rag/lab/requirements-aarch64.lock
docker --context orbstack exec enterprise-ai-security-dev /workspaces/enterprise-ai-security-architectures/runtime/bin/python products/banking-rag/lab/prepare_models.py --destination /workspaces/enterprise-ai-security-architectures/work/models
```

Run cached models/tests in a separate container with the **same named volume mounted read-only** and network disabled. No credentials, home mount or Docker socket is needed. `/tmp` is the disposable evidence output. The canonical runtime was created at the same volume path so its interpreter and libraries resolve in this verification container.

```sh
docker --context orbstack run --rm --network none --user 1000:1000 --read-only --cap-drop ALL --security-opt no-new-privileges --cpus 4 --memory 4g --pids-limit 256 --tmpfs /tmp:rw,nosuid,nodev,size=512m --volume enterprise-ai-security-workspace:/workspaces:ro --workdir /workspaces/enterprise-ai-security-architectures/repo --env PYTHONDONTWRITEBYTECODE=1 python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b /workspaces/enterprise-ai-security-architectures/runtime/bin/python products/banking-rag/lab/verify.py --output /tmp/banking-rag-check --models /workspaces/enterprise-ai-security-architectures/work/models --isolated
```

To retain output, use a named verification container while it runs, transfer the `/tmp` evidence to the canonical workspace, then remove that ephemeral container. Preserve the persistent workspace volume. This isolation is a property of the local tool run, not proof of physical air-gap or bank production security.
