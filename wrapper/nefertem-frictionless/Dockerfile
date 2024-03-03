FROM python:3.9

# Repo info
LABEL org.opencontainers.image.source=https://github.com/scc-digitalhub/digitalhub-core

# Set working dir
WORKDIR /app/

# Get digitalhub-sdk
ARG DHUB_VERSION=
RUN wget https://github.com/scc-digitalhub/digitalhub-sdk/archive/refs/tags/$DHUB_VERSION.zip | unzip
RUN mv digitalhub-sdk-$DHUB_VERSION digitalhub-sdk

# Install digitalhub-core, neferetem
RUN pip install digitalhub-sdk/core
RUN pip install digitalhub-sdk/data --no-deps
RUN pip install digitalhub-sdk/ --no-deps
RUN pip install digitalhub-sdk/data/modules/nefertem-frictionless[local]

# Install frictionless plugins
ARG NEFERTEM_VERSION=2.0.6
RUN wget https://github.com/scc-digitalhub/nefertem/archive/refs/tags/$NEFERTEM_VERSION.zip | unzip
RUN mv nefertem-$NEFERTEM_VERSION nefertem
RUN pip install ./nefertem/plugins/frictionless*

# Copy wrapper and set entry point
COPY wrapper.py /app/

# Cleanup folders
RUN rm -rf digitalhub-sdk $DHUB_VERSION.zip nefertem $NEFERTEM_VERSION.zip

ENTRYPOINT ["python", "wrapper.py"]
