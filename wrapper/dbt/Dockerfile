FROM python:3.9

# Repo info
LABEL org.opencontainers.image.source=https://github.com/scc-digitalhub/digitalhub-sdk
ARG VERSION=0.7.0b

# Set working dir
WORKDIR /app/

# Install runtime and requirements
RUN python -m pip install "digitalhub_runtime_dbt[local]>=${VERSION}"

# Copy wrapper and set entry point
COPY wrapper.py /app/

# Add nonroot group and user
RUN groupadd -r nrgroup && \
    useradd -r -m -g nrgroup nonroot && \
    chown -R nonroot:nrgroup /app
USER nonroot

ENTRYPOINT ["python", "wrapper.py"]
