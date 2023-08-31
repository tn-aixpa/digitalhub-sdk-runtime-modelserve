FROM ghcr.io/dbt-labs/dbt-core:latest

# Set working dir
WORKDIR /digitalhub-core/

RUN apt-get update && \
    apt-get install -y vim && \
    apt-get install -y python3.10 &&\
    rm -rf /var/lib/apt/lists/*

# Install dbt-postgres adapter via pip
RUN python -m pip install dbt-postgres 

# Install requests library
RUN python -m pip install requests

# Copy the shell script and make it executable
COPY create-user.sh /digitalhub-core/
RUN chmod +x /digitalhub-core/create-user.sh

COPY ./sdk ./sdk
RUN chmod -R 775 /digitalhub-core/sdk
RUN pip3 install ./sdk

# Copy wrapper and set entry point
COPY dbt_wrapper.py /digitalhub-core/

# Create the new user and set it as the default user
RUN /digitalhub-core/create-user.sh
USER dbt

ENTRYPOINT ["python", "dbt_wrapper.py"]
