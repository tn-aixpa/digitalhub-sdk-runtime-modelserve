FROM ghcr.io/dbt-labs/dbt-core:latest

# Set working dir
WORKDIR /digitalhub-core/

RUN apt-get update && \
    apt-get install -y vim && \
    apt-get install -y python3.10 &&\
    rm -rf /var/lib/apt/lists/*

#
RUN pip install --upgrade pip

# 
RUN python -m pip install dbt-postgres==1.6.3

# Copy and install sdk
COPY ./sdk ./lib
RUN chmod -R 775 /digitalhub-core/lib
RUN pip3 install -e ./lib

# Copy wrapper and set entry point
COPY wrapper.py /digitalhub-core/

# Create the new user and set it as the default user
RUN adduser --disabled-password --gecos "" dhcore
RUN chown -R dhcore: /digitalhub-core
USER dhcore

ENTRYPOINT ["python", "wrapper.py"]
