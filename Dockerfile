FROM python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b
WORKDIR /product
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.lock /product/requirements.lock
COPY vendor/wheels/ /wheels/
RUN python -m pip install --no-cache-dir --no-index --find-links=/wheels --require-hashes -r requirements.lock
COPY aiegateway/ /product/aiegateway/
COPY tools/ /product/tools/
COPY tests/ /product/tests/
COPY examples/ /product/examples/
COPY Dockerfile /product/Dockerfile
USER 65532:65532
CMD ["python", "-m", "aiegateway.demo"]
