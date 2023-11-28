FROM python:3.10-slim

# Repo info
LABEL org.opencontainers.image.source=https://github.com/scc-digitalhub/digitalhub-core

# Install git
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working dir
WORKDIR /digitalhub-core/

# Install digitalhub-core
RUN git clone https://github.com/scc-digitalhub/digitalhub-sdk.git
RUN pip3 install -e ./digitalhub-sdk/core
RUN pip3 install -e ./digitalhub-sdk/data/modules/nefertem[local]

# Install Nefertem plugins
RUN git clone https://github.com/scc-digitalhub/nefertem.git
RUN pip3 install -e ./nefertem/plugins/frictionless*
RUN pip3 install -e ./nefertem/plugins/duckdb*
RUN pip3 install -e ./nefertem/plugins/sqlalchemy*
RUN pip3 install -e ./nefertem/plugins/ydata*

# Copy wrapper and set entry point
COPY wrapper.py /digitalhub-core/

# Create the new user and set it as the default user
RUN adduser --disabled-password --gecos "" dhcore
RUN chown -R dhcore: /digitalhub-core
USER dhcore

ENTRYPOINT ["python", "wrapper.py"]
