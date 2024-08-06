FROM python:3.9

# Repo info
LABEL org.opencontainers.image.source=https://github.com/scc-digitalhub/oltreai-sdk
ARG VERSION=0.7.0b


# Set working dir
WORKDIR /app/

# Install oltreai-core
RUN python -m pip install "oltreai-core[full]>=${VERSION}" \
                          "oltreai-data[pandas]>=${VERSION}" \
                          "oltreai-runtime-kfp>=${VERSION}" && \
    python -m pip install "kfp==1.8.11" && \
    python -m pip install "oltreai>=${VERSION}" \
                          "oltreai-ml>=${VERSION}" \
                          "oltreai-runtime-python>=${VERSION}" \
                          "oltreai-runtime-mlrun>=${VERSION}" \
                          "oltreai-runtime-container>=${VERSION}" \
                          "oltreai-runtime-dbt>=${VERSION}" \
                          "oltreai-runtime-nefertem>=${VERSION}" --no-deps

# Copy wrapper and set entry point
COPY wrapper.py /app/
COPY step.py /app/

ENTRYPOINT ["python", "wrapper.py"]
