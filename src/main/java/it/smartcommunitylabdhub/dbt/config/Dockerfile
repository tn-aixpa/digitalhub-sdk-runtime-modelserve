FROM ghcr.io/dbt-labs/dbt-core:latest

# Set working dir
WORKDIR /app/

RUN apt-get update && \
    apt-get install -y vim && \
    rm -rf /var/lib/apt/lists/*

# Install dbt-postgres adapter via pip
RUN python -m pip install dbt-postgres 

# Install requests library
RUN python -m pip install requests

# Copy the shell script and make it executable
COPY create-user.sh /app/
RUN chmod +x /app/create-user.sh

# Create the new user and set it as the default user
RUN /app/create-user.sh
USER dbt

# Copy wrapper and set entry point
COPY dbt_wrapper.py /app/
ENTRYPOINT ["python", "dbt_wrapper.py"]
