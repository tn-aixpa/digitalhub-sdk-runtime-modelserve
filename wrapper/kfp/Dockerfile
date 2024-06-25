FROM python:3.9

# Repo info
LABEL org.opencontainers.image.source=https://github.com/scc-digitalhub/digitalhub-core
ARG DHUB_VERSION=

# Set working dir
WORKDIR /app/

# Install digitalhub-core
RUN python -m pip install digitalhub-core[full]==${DHUB_VERSION} \
                          digitalhub-data[pandas]==${DHUB_VERSION} \
                          digitalhub-runtime-kfp==${DHUB_VERSION} && \
    python -m pip install digitalhub==${DHUB_VERSION} \
                          digitalhub-ml==${DHUB_VERSION} \
                          digitalhub-runtime-python==${DHUB_VERSION} \
                          digitalhub-runtime-mlrun==${DHUB_VERSION} \
                          digitalhub-runtime-container==${DHUB_VERSION} \
                          digitalhub-runtime-dbt==${DHUB_VERSION} \
                          digitalhub-runtime-nefertem==${DHUB_VERSION} --no-deps

# Copy wrapper and set entry point
COPY wrapper.py /app/
COPY step.py /app/

ENTRYPOINT ["python", "wrapper.py"]
