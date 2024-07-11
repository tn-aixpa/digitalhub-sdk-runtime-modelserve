FROM python:3.9

# Repo info
LABEL org.opencontainers.image.source=https://github.com/scc-digitalhub/digitalhub-core
ARG DHUB_VERSION=
ARG BASE_VER=0.6.0b
ARG VERSION=0.6.0b5


# Set working dir
WORKDIR /app/

# Install digitalhub-core
RUN python -m pip install "digitalhub-core[full]>=${BASE_VER}" \
                          "digitalhub-data[pandas]>=${BASE_VER}" \
                          digitalhub-runtime-kfp==${VERSION} && \
    python -m pip install "digitalhub>=${BASE_VER}" \
                          "digitalhub-ml>=${BASE_VER}" \
                          "digitalhub-runtime-python>=${BASE_VER}" \
                          "digitalhub-runtime-mlrun>=${BASE_VER}" \
                          "digitalhub-runtime-container>=${BASE_VER}" \
                          "digitalhub-runtime-dbt>=${BASE_VER}" \
                          "digitalhub-runtime-nefertem>=${BASE_VER}" --no-deps

# Copy wrapper and set entry point
COPY wrapper.py /app/
COPY step.py /app/

ENTRYPOINT ["python", "wrapper.py"]
