import subprocess
import os
import json
import base64
import requests
import sys
import re
import dataclasses
import uuid as uuid4


from dbt.cli.main import dbtRunner, dbtRunnerResult
from datetime import datetime
from enum import Enum


# Define a custom JSON encoder to handle complex types
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


# Function to make a POST request
def make_post_request(base_url, endpoint, data=None):
    url = f"{base_url}/{endpoint}"
    response = requests.post(url, json=data)
    return response


# Function to make a GET request with parameters in the URL path
def make_get_request(base_url, endpoint, *path_params):
    url = f"{base_url}/{endpoint}/{'/'.join(path_params)}"
    response = requests.get(url)
    return response


# Function to make a PUT request
def make_put_request(base_url, endpoint, data=None, *path_params):
    url = f"{base_url}/{endpoint}/{'/'.join(path_params)}"
    response = requests.put(url, json=data)
    return response


# Get run from dh_core
def get_run() -> dict:
    # Call an external HTTP service to retrieve information

    DH_CORE = os.environ.get("DH_CORE")
    RUN_ID = os.environ.get("RUN_ID")
    response = make_get_request(DH_CORE, "api/v1/runs", RUN_ID)

    print("==================== GET RUN =====================")
    print(f"{response.json()}")
    return response.json()


def create_dataitem(data: dict) -> dict:
    DH_CORE = os.environ.get("DH_CORE")
    response = make_post_request(DH_CORE, "api/v1/dataitems", data)

    print("==================== DATAITEM =====================")
    print(f"{response.json()}")
    return response.json()


def update_run(run_id: str, run: dict) -> dict:
    DH_CORE = os.environ.get("DH_CORE")
    response = make_put_request(DH_CORE, "api/v1/runs", run, run_id)

    print(f"{response.json()}")
    return response


def parse_dbt_url(url):
    # Define a regular expression pattern to match the URL structure
    pattern = r"(?P<kind>[\w-]+)://(?P<project>[\w-]+)/(?P<function>[\w-]+):(?P<version>[\w-]+)"

    # Use regex to extract components from the URL
    match = re.match(pattern, url)

    if match:
        return match.groupdict()
    else:
        return None


def initialize_project(run: dict, uuid: str) -> None:
    spec: dict = run.get("spec", {})
    dbt: dict = spec.get("dbt", {})

    outputs = spec.get("outputs").get("dataitems", ["output"])
    inputs = spec.get("inputs").get("dataitems", ["input"])

    # Parse task string
    task_accessor = parse_dbt_url(run.get("task"))

    # Get project name
    project_name = task_accessor.get("project", "default_name").replace("-", "_")

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
    # to clean project add clean-targets: [target, dbt_packages, logs]
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

    # Decode and write the base64-encoded model_sql to the file
    model_sql = dbt.get("sql", "")
    decoded_model_sql = base64.b64decode(model_sql).decode("UTF-8")
    with open(
        f"{models_directory}/{outputs[0]}.sql",
        "w",
    ) as schema_file:
        schema_file.write(decoded_model_sql)

    # write schema and version detail for outputs versioning
    with open(f"{models_directory}/{outputs[0]}.yml", "w") as schema_def:
        schema_def.write(
            """         
models:
  - name: {model_name}
    latest_version: {uuid}
    versions: 
        - v: {uuid}
          config:
            materialized: table
      """.format(
                model_name=outputs[0], uuid=uuid
            )
        )

    # write schema and version detail ( qui forse va l'input)
    with open(f"{models_directory}/{inputs[0]}.yml", "w") as schema_def:
        schema_def.write(
            """         
models:
  - name: {model_name}
    latest_version: 9e5902e5-61db-4e42-89c1-adefc5500ae6
    versions: 
        - v: 9e5902e5-61db-4e42-89c1-adefc5500ae6
          config:
            materialized: table
      """.format(
                model_name=inputs[0]
            )
        )

    # write all version of sql selects
    with open(
        f"{models_directory}/{inputs[0]}_v9e5902e5-61db-4e42-89c1-adefc5500ae6.sql", "w"
    ) as schema_def:
        schema_def.write(
            f'select * from "{inputs[0]}_v9e5902e5-61db-4e42-89c1-adefc5500ae6"'
        )


def main() -> None:
    print("Initializing dbt project and running it...")

    # retrieve the run from core
    run: dict = get_run()
    spec: dict = run.get("spec", {})
    outputs = spec.get("outputs").get("dataitems", ["output"])
    # generate uuid for dataitem
    uuid: str = str(uuid4.uuid4())

    print(f"this id DATAITEM UUID : {uuid}")

    # TODO: with input I have to import all the dataitem for the query
    inputs = spec.get("inputs").get("dataitems", ["input"])

    # Parse task string
    task_accessor = parse_dbt_url(run.get("task"))

    # Get project name
    project_name = task_accessor.get("project", "default_name").replace("-", "_")

    # initialize project
    initialize_project(run=run, uuid=uuid)

    # initialize dbt Runner
    dbt = dbtRunner()

    # clean dbt
    dbt.invoke("clean")

    # create CLI args as a list of strings
    cli_args = ["run", "--select", f"{outputs[0]}"]

    # run dbt
    res: dbtRunnerResult = dbt.invoke(cli_args)

    # inspect the results
    json_results = []
    for r in res.result:
        json_string = json.dumps(dataclasses.asdict(r), cls=CustomJSONEncoder, indent=2)
        json_results.append(json.loads(json_string))

    try:
        # first check if we have results
        if len(json_results) > 0:
            # check status is success
            result = json_results[-1]
            if (
                result.get("status") == "success"
                and result.get("node").get("package_name") == project_name
                and result.get("node").get("name") == outputs[0]
            ):
                print(f"SUCCESSFUL -> Send info to core backend")

                components = [
                    component.strip('"')
                    for component in result.get("node").get("relation_name").split(".")
                ]

                raw_code = base64.b64encode(
                    result.get("node").get("raw_code", "").encode("utf-8")
                )
                compiled_code = base64.b64encode(
                    result.get("node").get("compiled_code", "").encode("utf-8")
                )

                dataitem = {
                    "id": uuid,
                    "name": result.get("node").get("name"),
                    "project": task_accessor.get("project"),
                    "kind": "sql",
                    "spec": {
                        "path": f"sql://postgres/{'/'.join(components)}",
                        "raw_code": raw_code.decode("utf-8"),
                        "compiled_code": compiled_code.decode("utf-8"),
                    },
                    "state": result.get("status", "none").upper(),
                }

                # store dataitem into dh core
                dataitem_result = create_dataitem(data=dataitem)

                # Extract timing information
                timing = result.get("timing", [])
                compile_timing = None
                execute_timing = None

                for entry in timing:
                    if entry.get("name") == "compile":
                        compile_timing = entry
                    elif entry.get("name") == "execute":
                        execute_timing = entry

                # update run with dataitems result
                run.update(
                    {
                        "status": {
                            "dataitems": [
                                {
                                    "key": outputs[0],
                                    "kind": "dataitem",
                                    "id": f"store://{dataitem_result.get('project')}/dataitems/{dataitem_result.get('name')}:{dataitem_result.get('id')}",
                                }
                            ],
                            "timing": {
                                "compile": {
                                    "started_at": compile_timing.get("started_at"),
                                    "completed_at": compile_timing.get("completed_at"),
                                },
                                "execute": {
                                    "started_at": execute_timing.get("started_at"),
                                    "completed_at": execute_timing.get("completed_at"),
                                },
                            },
                        },
                    }
                )

                print("======================= UPDATE RUN ========================")
                print(run)
                update_run(run.get("id"), run)

            else:
                # check project and model name match
                print(
                    "ERROR -> Execution is not successful or got wrong project name or function name."
                )
        else:
            print("ERROR -> No results found.")

    except:
        print("Something got wrong during object result access")

    # TODO: devo verificare che fqn=['default_name', 'output'],  ho preso il progetto giusto con il modello giusto.

    # se e' giusto passo lo status della run al backend (core) [status, timing]
    # ci interessa l'esito (success/error), metadata sull'esecuzione (es execution time), tipo di output (es output)
    #       'adapter_response': {'_message': 'CREATE VIEW', 'code': 'CREATE VIEW', 'rows_affected': -1},
    #       'message': 'CREATE VIEW',

    # del modello ci interessa il path come dataitem sql://postgres......  relation_name='"dbt"."public"."output"',
    # ci interessa inoltre il raw_code e il compiled_code ( va messo tutto in extra )

    sys.exit(0)


if __name__ == "__main__":
    main()
