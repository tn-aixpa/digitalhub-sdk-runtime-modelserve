FROM python:3.10-slim

# Repo info
LABEL org.opencontainers.image.source=https://github.com/scc-digitalhub/digitalhub-core

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working dir
WORKDIR /digitalhub-core/

# Copy and install sdk-dbt and sdk
RUN python -m pip install "git+https://github.com/scc-digitalhub/digitalhub-core.git#egg=digitalhub_core&subdirectory=sdk"
RUN python -m pip install "git+https://github.com/scc-digitalhub/digitalhub-core.git#egg=digitalhub_core_dbt&subdirectory=sdk/modules/dbt"

# Copy wrapper and set entry point
COPY wrapper.py /digitalhub-core/

# Create the new user and set it as the default user
RUN adduser --disabled-password --gecos "" dhcore
RUN chown -R dhcore: /digitalhub-core
USER dhcore

ENTRYPOINT ["python", "wrapper.py"]
