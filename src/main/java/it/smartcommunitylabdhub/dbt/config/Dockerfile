FROM ghcr.io/dbt-labs/dbt-core:latest

# Set environment variables
ENV DBT_DB_HOST=postgres
ENV DBT_DB_USER=testuser
ENV DBT_DB_PASS=testpassword
ENV DBT_DB_PORT=5432
ENV DBT_DB_NAME=dbt

# Set working dir
WORKDIR /app/

# Install dbt-postgres adapter via pip
RUN python -m pip install dbt-postgres 

# Copy the shell script and make it executable
COPY create-user.sh /app/
RUN chmod +x /app/create-user.sh

# Create the new user and set it as the default user
RUN /app/create-user.sh
USER dbt

# Copy wrapper and set entry point
COPY dbt_wrapper.py /app/
ENTRYPOINT ["python", "dbt_wrapper.py"]
