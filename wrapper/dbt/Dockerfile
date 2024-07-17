FROM python:3.9

# Repo info
LABEL org.opencontainers.image.source=https://github.com/scc-digitalhub/digitalhub-core
ARG DHUB_VERSION=
ARG VERSION=0.6.0b

# Set working dir
WORKDIR /app/

# Install runtime and requirements
RUN python -m pip install "digitalhub_runtime_dbt[local]>=${VERSION}"

# Copy wrapper and set entry point
COPY wrapper.py /app/

ENTRYPOINT ["python", "wrapper.py"]
