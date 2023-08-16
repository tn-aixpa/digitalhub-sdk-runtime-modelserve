import subprocess
import os
import json
import base64
import requests
import sys
import re

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

    print(f"{response.json()}")
    return response.json()


def post_dataitem(data: dict) -> dict:
    DH_CORE = os.environ.get("DH_CORE")
    response = make_post_request(DH_CORE, "api/v1/dataitems", data)

    print(f"{response.json()}")
    return response.json()


def put_run(run_id: str, run: dict) -> dict:
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


def initialize_project(run: dict) -> None:
    spec: dict = run.get("spec", {})
    dbt: dict = spec.get("dbt", {})

    output_name = spec.get("output", "model")

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
    with open(f"{models_directory}/{output_name}.sql", "w") as schema_file:
        schema_file.write(decoded_model_sql)


def extract_response(res) -> dict:
    # Extract relevant information manually
    return {
        "status": res.status,
        "timing": [
            {
                "name": timing.name,
                "started_at": timing.started_at.isoformat(),
                "completed_at": timing.completed_at.isoformat(),
            }
            for timing in res.timing
        ],
        "thread_id": res.thread_id,
        "execution_time": res.execution_time,
        "adapter_response": res.adapter_response,
        "message": res.message,
        "failures": res.failures,
        "node": {
            "database": res.node.database,
            "schema": res.node.schema,
            "name": res.node.name,
            "resource_type": res.node.resource_type,
            "package_name": res.node.package_name,
            "path": res.node.path,
            "original_file_path": res.node.original_file_path,
            "unique_id": res.node.unique_id,
            "fqn": res.node.fqn,
            "alias": res.node.alias,
            "checksum": {
                "name": res.node.checksum.name,
                "checksum": res.node.checksum.checksum,
            },
            "config": {
                "_extra": res.node.config._extra,
                "enabled": res.node.config.enabled,
                "alias": res.node.config.alias,
                "schema": res.node.config.schema,
                "database": res.node.config.database,
                "tags": res.node.config.tags,
                "meta": res.node.config.meta,
                "group": res.node.config.group,
                "materialized": res.node.config.materialized,
                "incremental_strategy": res.node.config.incremental_strategy,
                "persist_docs": res.node.config.persist_docs,
                "post_hook": res.node.config.post_hook,
                "pre_hook": res.node.config.pre_hook,
                "quoting": res.node.config.quoting,
                "column_types": res.node.config.column_types,
                "full_refresh": res.node.config.full_refresh,
                "unique_key": res.node.config.unique_key,
                "on_schema_change": res.node.config.on_schema_change,
                "on_configuration_change": res.node.config.on_configuration_change,
                "grants": res.node.config.grants,
                "packages": res.node.config.packages,
                "docs": {
                    "show": res.node.config.docs.show,
                    "node_color": res.node.config.docs.node_color,
                },
                "contract": {
                    "enforced": res.node.config.contract.enforced,
                },
            },
            "_event_status": res.node._event_status,
            "tags": res.node.tags,
            "description": res.node.description,
            "columns": res.node.columns,
            "meta": res.node.meta,
            "group": res.node.group,
            "docs": {
                "show": res.node.docs.show,
                "node_color": res.node.docs.node_color,
            },
            "patch_path": res.node.patch_path,
            "build_path": res.node.build_path,
            "deferred": res.node.deferred,
            "unrendered_config": res.node.unrendered_config,
            "created_at": res.node.created_at,
            "config_call_dict": res.node.config_call_dict,
            "relation_name": res.node.relation_name,
            "raw_code": res.node.raw_code,
            "language": res.node.language,
            "refs": res.node.refs,
            "sources": res.node.sources,
            "metrics": res.node.metrics,
            "depends_on": {
                "macros": res.node.depends_on.macros,
                "nodes": res.node.depends_on.nodes,
            },
            "compiled_path": res.node.compiled_path,
            "compiled": res.node.compiled,
            "compiled_code": res.node.compiled_code,
            "extra_ctes_injected": res.node.extra_ctes_injected,
            "extra_ctes": res.node.extra_ctes,
            "_pre_injected_sql": res.node._pre_injected_sql,
            "contract": {
                "enforced": res.node.contract.enforced,
                "checksum": res.node.contract.checksum,
            },
            "access": res.node.access,
            "constraints": res.node.constraints,
            "version": res.node.version,
            "latest_version": res.node.latest_version,
            "deprecation_date": res.node.deprecation_date,
            "defer_relation": res.node.defer_relation,
        },
    }


def main() -> None:
    print("Initializing dbt project and running it...")

    # retrieve the run from core
    run: dict = get_run()
    spec: dict = run.get("spec", {})

    # Parse task string
    task_accessor = parse_dbt_url(run.get("task"))

    # Get project name
    project_name = task_accessor.get("project", "default_name").replace("-", "_")

    # initialize project
    initialize_project(run=run)

    # initialize dbt Runner
    dbt = dbtRunner()

    # create CLI args as a list of strings
    cli_args = ["run"]

    # run dbt
    res: dbtRunnerResult = dbt.invoke(cli_args)

    # inspect the results
    json_results = []
    for r in res.result:
        json_string = json.dumps(extract_response(r), cls=CustomJSONEncoder, indent=2)
        json_results.append(json.loads(json_string))

    print(f"{json_results}")

    try:
        # first check if we have results
        if len(json_results) > 0:
            # check status is success
            result = json_results[0]
            if (
                result.get("status") == "success"
                and result.get("node").get("package_name") == project_name
                and result.get("node").get("name") == spec.get("output", "model")
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
                dataitem_result = post_dataitem(data=dataitem)

                # update run with dataitems result
                run.update(
                    {
                        "dataitems": [
                            {
                                "key": "dataitem",
                                "kind": "dataitem",
                                "id": f"store://{dataitem_result.get('project')}/dataitems/{dataitem_result.get('name')}:{dataitem_result.get('id')}",
                            }
                        ]
                    }
                )

                print("======================= UPDATE RUN ========================")
                print(run)
                put_run(run.get("id"), run)

            else:
                # check project and model name match
                print(
                    "ERROR -> Execution is not successful or got wrong project name or function name."
                )
        else:
            print("ERROR -> No results found.")

    except:
        print("Something got wrong during object result access")

    # TODO: devo verificare che fqn=['default_name', 'model'],  ho preso il progetto giusto con il modello giusto.

    # se e' giusto passo lo status della run al backend (core) [status, timing]
    # ci interessa l'esito (success/error), metadata sull'esecuzione (es execution time), tipo di output (es model)
    #       'adapter_response': {'_message': 'CREATE VIEW', 'code': 'CREATE VIEW', 'rows_affected': -1},
    #       'message': 'CREATE VIEW',

    # del modello ci interessa il path come dataitem sql://postgres......  relation_name='"dbt"."public"."model"',
    # ci interessa inoltre il raw_code e il compiled_code ( va messo tutto in extra )

    sys.exit(0)


if __name__ == "__main__":
    main()
