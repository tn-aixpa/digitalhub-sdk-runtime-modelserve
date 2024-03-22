FROM python:3.9

# Repo info
LABEL org.opencontainers.image.source=https://github.com/scc-digitalhub/digitalhub-core

# Set working dir
WORKDIR /app/

# Get digitalhub-sdk
ARG DHUB_VERSION=
RUN wget https://github.com/scc-digitalhub/digitalhub-sdk/archive/refs/tags/$DHUB_VERSION.zip
RUN unzip $DHUB_VERSION.zip
RUN mv digitalhub-sdk-$DHUB_VERSION digitalhub-sdk

# Install digitalhub-core
RUN pip install ./digitalhub-sdk/ --no-deps
RUN pip install ./digitalhub-sdk/core
RUN pip install ./digitalhub-sdk/core/modules/kfp
RUN pip install ./digitalhub-sdk/core/modules/container --no-deps
# Install digitalhub-data, and modules
RUN pip install ./digitalhub-sdk/data --no-deps
RUN pip install ./digitalhub-sdk/data/modules/* --no-deps
# Install digitalhub-ml, and modules
RUN pip install ./digitalhub-sdk/ml/ --no-deps
RUN pip install ./digitalhub-sdk/ml/modules/* --no-deps

# Copy wrapper and set entry point
COPY wrapper.py /app/
COPY step.py /app/

# Cleanup
RUN rm -rf digitalhub-sdk $DHUB_VERSION.zip

ENTRYPOINT ["python", "wrapper.py"]
