FROM python:3.9

# Repo info
LABEL org.opencontainers.image.source=https://github.com/scc-digitalhub/digitalhub-core
ARG DHUB_VERSION=
ARG VERSION=0.6.0b


# Set working dir
WORKDIR /app/

# Install digitalhub-core
RUN python -m pip install "digitalhub-core[full]>=${VERSION}" \
                          "digitalhub-data[pandas]>=${VERSION}" \
                          "digitalhub-runtime-kfp>=${VERSION}" && \
    python -m pip install "digitalhub>=${VERSION}" \
                          "digitalhub-ml>=${VERSION}" \
                          "digitalhub-runtime-python>=${VERSION}" \
                          "digitalhub-runtime-mlrun>=${VERSION}" \
                          "digitalhub-runtime-container>=${VERSION}" \
                          "digitalhub-runtime-dbt>=${VERSION}" \
                          "digitalhub-runtime-nefertem>=${VERSION}" --no-deps

# Copy wrapper and set entry point
COPY wrapper.py /app/
COPY step.py /app/

ENTRYPOINT ["python", "wrapper.py"]
