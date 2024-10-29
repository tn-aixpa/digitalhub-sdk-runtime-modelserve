ARG VERSION=
FROM ghcr.io/scc-digitalhub/digitalhub-serverless/python-runtime:3.11-${VERSION}

ARG ROOT=/opt/conda/lib/python3.11/site-packages

COPY ./digitalhub-sdk/digitalhub ${ROOT}/digitalhub
COPY ./digitalhub-sdk/runtimes/python/digitalhub_runtime_python ${ROOT}/digitalhub_runtime_python
COPY ./digitalhub-sdk/runtimes/container/digitalhub_runtime_container ${ROOT}/digitalhub_runtime_container
COPY ./digitalhub-sdk/runtimes/kfp/digitalhub_runtime_kfp ${ROOT}/digitalhub_runtime_kfp
COPY ./digitalhub-sdk/runtimes/dbt/digitalhub_runtime_dbt ${ROOT}/digitalhub_runtime_dbt
COPY ./digitalhub-sdk/runtimes/modelserve/digitalhub_runtime_modelserve ${ROOT}/digitalhub_runtime_modelserve
