FROM python:3.9

# Repo info
LABEL org.opencontainers.image.source=https://github.com/scc-digitalhub/digitalhub-core

# Set working dir
WORKDIR /digitalhub-core/

# Get digitalhub-sdk
ARG DHUB_VERSION=0.0.8
RUN wget https://github.com/scc-digitalhub/digitalhub-sdk/archive/refs/tags/v$DHUB_VERSION.zip
RUN unzip v$DHUB_VERSION.zip
RUN mv digitalhub-sdk-$DHUB_VERSION digitalhub-sdk

# Install digitalhub-core, dbt
RUN pip3 install -e ./digitalhub-sdk/core[dbt_yaml]
RUN pip3 install -e ./digitalhub-sdk/data/modules/dbt[local]

# Copy wrapper and set entry point
COPY wrapper.py /digitalhub-core/

# Cleanup
RUN rm -rf digitalhub-sdk nefertem

ENTRYPOINT ["python", "wrapper.py"]
