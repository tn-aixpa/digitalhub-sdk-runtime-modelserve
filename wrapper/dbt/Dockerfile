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

# Use non root user
RUN chown -R 1000 /app
USER 1000

ENTRYPOINT ["python", "wrapper.py"]
