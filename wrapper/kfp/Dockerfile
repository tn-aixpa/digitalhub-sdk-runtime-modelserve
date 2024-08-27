FROM python:3.9

# Repo info
LABEL org.opencontainers.image.source=https://github.com/scc-digitalhub/digitalhub-sdk
ARG VERSION=0.7.0b


# Set working dir
WORKDIR /app/

# Install digitalhub-core
RUN python -m pip install "digitalhub-core[full]>=${VERSION}" \
                          "digitalhub-data[pandas]>=${VERSION}" \
                          "digitalhub-runtime-kfp[local]>=${VERSION}" && \
    python -m pip install "digitalhub>=${VERSION}" \
                          "digitalhub-ml>=${VERSION}" \
                          "digitalhub-runtime-python>=${VERSION}" \
                          "digitalhub-runtime-container>=${VERSION}" \
                          "digitalhub-runtime-modelserve>=${VERSION}" \
                          "digitalhub-runtime-dbt>=${VERSION}" --no-deps

# Copy wrapper and set entry point
COPY wrapper.py /app/
COPY step.py /app/

ENTRYPOINT ["python", "wrapper.py"]
