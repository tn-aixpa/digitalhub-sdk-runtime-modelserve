import subprocess
import os
import json
import base64
from dbt.cli.main import dbtRunner, dbtRunnerResult
from datetime import datetime

from io import StringIO


def initialize_project():
    # Call an external HTTP service to retrieve information
    # response = requests.get("http://core-service")
    # data = response.json()
    data = json.loads(
        '{"metadata":{"project":"dh_core"},"spec":{"dbt":{"sql":"Cnt7IGNvbmZpZyhtYXRlcmlhbGl6ZWQ9J3ZpZXcnKSB9fQoKd2l0aCBpdGFseV9jaXRpZXMgYXMgKAogICAgU0VMRUNUIAogICAgICAgIGMuY2l0eV9uYW1lIGFzIGNpdHksIAogICAgICAgIHIucmVnaW9uX25hbWUgYXMgcmVnaW9uLCAKICAgICAgICBzLnN0YXRlX25hbWUgYXMgc3RhdGUgCiAgICBGUk9NIGNpdGllcyBjCiAgICBKT0lOIHJlZ2lvbnMgciBPTiBjLnJlZ2lvbl9pZCA9IHIucmVnaW9uX2lkCiAgICBKT0lOIHN0YXRlcyBzIE9OIHIuc3RhdGVfaWQgPSBzLnN0YXRlX2lkCiAgICBXSEVSRSBzLnN0YXRlX25hbWUgPSAnSXRhbHknCikKCnNlbGVjdCAqIGZyb20gaXRhbHlfY2l0aWVzCg=="}}}',
        strict=False,
    )
    spec = data.get("spec", {})
    dbt = spec.get("dbt", {})
    metadata = spec.get("metadata", {})

    # Get project name
    project_name = metadata.get("project", "default_name")

    # Create dbt profiles.yml

    with open(f"profiles.yml", "w") as profiles_file:
        profiles_file.write(
            """
postgres:
    outputs:
        dev:
            type: postgres
            host: {db_host}
            user: {db_user}
            pass: {db_pass}
            port: {db_port}
            dbname: {db_name}
            schema: public
    target: dev
        """.format(
                db_host=os.environ["POSTGRES_DB_HOST"],
                db_user=os.environ["POSTGRES_USER"],
                db_pass=os.environ["POSTGRES_PASSWORD"],
                db_port=os.environ["POSTGRES_PORT"],
                db_name=os.environ["POSTGRES_DB"],
            )
        )

    # Create dbt_project.yml from 'dbt'
    with open(f"dbt_project.yml", "w") as dbt_project_file:
        dbt_project_file.write(
            """
name: "{project_name}"
version: "1.0.0"
config-version: 2
profile: "postgres"
model-paths: ["models"]
models:
        """.format(
                project_name=project_name
            )
        )

    # Create a new folder in models directory and put a schema.yml definition
    models_directory = "models"
    os.makedirs(models_directory, exist_ok=True)

    # Create model schema.yml from 'spec'
    model_sql = dbt.get("sql", {})
    with open(f"{models_directory}/model.sql", "w") as schema_file:
        schema_file.write(base64.b64decode(model_sql).decode("UTF-8"))


def format_response(res):
    return {}


def main():
    print("Initializing dbt project and running it...")
    initialize_project()

    # initialize
    dbt = dbtRunner()

    # create CLI args as a list of strings
    cli_args = ["run"]

    # run the command
    res: dbtRunnerResult = dbt.invoke(cli_args)

    results_json = []
    # inspect the results
    for r in res.result:
        # results_json.append(format_response(r))

        print(f"{r}")
        # print(f"{r.node.name}: {r.status}")

    print(f"{results_json}")
    # call api to store result


if __name__ == "__main__":
    main()
