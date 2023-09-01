from __future__ import annotations

import base64
import os
import typing
from pathlib import Path
from uuid import uuid4

from dbt.cli.main import dbtRunner, dbtRunnerResult

import sdk

if typing.TYPE_CHECKING:
    from dbt.contracts.results import RunResult
    from sdk.entities.dataitem.entity import Dataitem
    from sdk.entities.run.entity import Run
    from sdk.entities.run.spec.base import RunSpec


####################
# Constants
####################

MODELS_DIRECTORY = Path("models")
RUN_ID = os.environ.get("RUN_ID")
PROJECT_NAME = os.environ.get("PROJECT_NAME")
DATAITEM_DBT = "dbt"

# Postgres
PG_HOST = os.environ["POSTGRES_DB_HOST"]
PG_PORT = os.environ["POSTGRES_PORT"]
PG_USER = os.environ["POSTGRES_USER"]
PG_PSWD = os.environ["POSTGRES_PASSWORD"]
PG_DB = os.environ["POSTGRES_DB"]

####################
# Set up environment
####################

# Create models directory
MODELS_DIRECTORY.mkdir(parents=True, exist_ok=True)

# Set up sql store
cnstr = f"postgresql://{PG_USER}:{PG_PSWD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
cfg = {"connection_string": cnstr}
stcfg = sdk.StoreConfig(
    name="sql",
    type="sql",
    uri=f"sql://postgres/{PG_DB}/public",
    is_default=True,
    config=cfg,
)
sdk.set_store(stcfg)

# Set up s3 store
st = {
    "endpoint_url": os.environ["S3_ENDPOINT"],
    "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
    "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
}
cfg = sdk.StoreConfig(
    name="s3", type="s3", uri="s3://mlrun/", is_default=False, config=st
)
sdk.set_store(cfg)


####################
# IO functions
####################


def materialize_inputs(inputs: list) -> None:
    """
    Materialize inputs in postgres.

    Parameters
    ----------
    inputs : list
        The list of inputs.

    Returns
    -------
    None
    """
    for name in inputs:
        try:
            di = sdk.get_dataitem(PROJECT_NAME, name)
        except Exception:
            raise RuntimeError(f"Dataitem {name} not found in project {PROJECT_NAME}")
        df = di.as_df()
        target_path = f"sql://postgres/{PG_DB}/public/{name}_v{di.id}"
        try:
            di.write_df(df, target_path)
        except:
            pass


####################
# Templates for dbt
####################

PROJECT_TEMPLATE = """
name: "{}"
version: "1.0.0"
config-version: 2
profile: "postgres"
model-paths: ["{}"]
models:
"""
MODEL_TEMPLATE_UUID = """
models:
  - name: {}
    latest_uuid: {}
    uuids:
        - v: {}
          config:
            materialized: table
"""
MODEL_TEMPLATE_VERSION = """
models:
  - name: {}
    latest_version: {}
    versions:
        - v: {}
          config:
            materialized: table
"""
PROFILE_TEMPLATE = f"""
postgres:
    outputs:
        dev:
            type: postgres
            host: {PG_HOST}
            user: {PG_USER}
            pass: {PG_PSWD}
            port: {PG_PORT}
            dbname: {PG_DB}
            schema: public
    target: dev
"""


def generate_inputs_conf(inputs: list) -> None:
    """
    Generate inputs confs dependencies for dbt project.

    Parameters
    ----------
    inputs : list
        The list of inputs.

    Returns
    -------
    None
    """
    for name in inputs:
        # Get dataitem from core
        response = sdk.get_dataitem(PROJECT_NAME, name)
        uuid = response.id

        # write schema and version detail for inputs versioning
        input_path = Path(MODELS_DIRECTORY, f"{name}.sql")
        input_path.write_text(MODEL_TEMPLATE_UUID.format(name, uuid, uuid))

        # write also sql select for the schema
        sql_path = Path(MODELS_DIRECTORY, f"{name}_v{uuid}.sql")
        sql_path.write_text(f'SELECT * FROM "{name}_v{uuid}"')


def generate_outputs_conf(sql: str, output: str, uuid: str) -> None:
    """
    Write sql code for the model and write schema
    and version detail for outputs versioning

    Parameters
    ----------
    sql : str
        The sql code.
    output : str
        The output table name.
    uuid : str
        The uuid of the model for outputs versioning.

    Returns
    -------
    None
    """
    sql_path = Path(MODELS_DIRECTORY, f"{output}.sql")
    sql_path.write_text(sql)

    output_path = Path(MODELS_DIRECTORY, f"{output}.yml")
    output_path.write_text(MODEL_TEMPLATE_VERSION.format(output, uuid, uuid))


def generate_dbt_project_yml() -> None:
    """
    Create dbt_project.yml from 'dbt'

    Returns
    -------
    None
    """
    # to clean project add clean-targets: [target, dbt_packages, logs]
    project_path = Path("dbt_project.yml")
    project_path.write_text(
        PROJECT_TEMPLATE.format(PROJECT_NAME.replace("-", "_"), MODELS_DIRECTORY)
    )


def generate_dbt_profile_yml() -> None:
    """
    Create dbt profiles.yml

    Returns
    -------
    None
    """
    profile_path = Path("profiles.yml")
    profile_path.write_text(PROFILE_TEMPLATE)


####################
# Functions for dbt
####################


def initialize_dbt_project(sql: str, inputs: list, output: str, uuid: str) -> None:
    """
    Initialize a dbt project with a model and a schema definition.

    Parameters
    ----------
    sql : str
        The sql code.
    inputs : list
        The list of inputs.
    output : str
        The output table name.
    uuid : str
        The uuid of the model for outputs versioning.

    Returns
    -------
    None
    """
    # Generate profile yaml file
    generate_dbt_profile_yml()

    # Generate project yaml file
    generate_dbt_project_yml()

    # Generate outputs confs
    generate_outputs_conf(sql, output, uuid)

    # Generate inputs confs
    generate_inputs_conf(inputs)


def execute_dbt_project(output: str) -> dbtRunnerResult:
    """
    Execute a dbt project with the specified outputs.
    It initializes a dbt runner, cleans the project and runs it.

    Parameters
    ----------
    output : str
        The output table name.

    Returns
    -------
    dbtRunnerResult
        An object representing the result of the dbt execution.
    """
    dbt = dbtRunner()
    dbt.invoke("clean")
    cli_args = ["run", "--select", f"{output}"]
    return dbt.invoke(cli_args)


####################
# Functions for parsing dbt results
####################


def parse_dbt_results(run_result: dbtRunnerResult, output: str) -> RunResult:
    """
    Parse dbt results.

    Parameters
    ----------
    run_result : dbtRunnerResult
        The dbt result.
    output : str
        The output table name.

    Returns
    -------
    RunResult
        Run result.
    """
    # Take last result, final result of the query
    try:
        result: RunResult = run_result.result[-1]
    except IndexError:
        raise RuntimeError("No results found.")

    if not result.status.value == "success":
        raise RuntimeError("Execution is not successfull.")

    if not result.node.package_name == PROJECT_NAME.replace("-", "_"):
        raise RuntimeError("Wrong project name.")

    if not result.node.name == output:
        raise RuntimeError("Wrong function name.")

    print("Send info to core backend")
    return result


def get_path(result: RunResult) -> str:
    """
    Get path from dbt result (sql://postgres/database/schema/table).

    Parameters
    ----------
    result : RunResult
        The dbt result.

    Returns
    -------
    str
        SQL path.
    """
    components = result.node.relation_name.replace('"', "")
    components = "/".join(components.split("."))
    return f"sql://postgres/{components}"


def get_code(result: RunResult) -> tuple:
    """
    Get code from dbt result.

    Parameters
    ----------
    result : RunResult
        The dbt result.

    Returns
    -------
    tuple
        A tuple containing raw and compiled code.
    """
    raw_code = base64.b64encode(result.node.raw_code.encode("utf-8"))
    compiled_code = base64.b64encode(result.node.compiled_code.encode("utf-8"))
    return raw_code, compiled_code


def get_timings(result: RunResult) -> dict:
    """
    Get timings from dbt result.

    Parameters
    ----------
    result : RunResult
        The dbt result.

    Returns
    -------
    dict
        A dictionary containing timings.
    """
    compile_timing = None
    execute_timing = None
    for entry in result.timing:
        if entry.name == "compile":
            compile_timing = entry
        elif entry.name == "execute":
            execute_timing = entry
    return {
        "timing": {
            "compile": {
                "started_at": compile_timing.started_at.isoformat(),
                "completed_at": compile_timing.completed_at.isoformat(),
            },
            "execute": {
                "started_at": execute_timing.started_at.isoformat(),
                "completed_at": execute_timing.completed_at.isoformat(),
            },
        }
    }


def get_dataitem_info(output: str, dataitem: Dataitem) -> dict:
    """
    Create dataitem info.

    Parameters
    ----------
    output : str
        The output table name.
    dataitem : Dataitem
        The dataitem.
    """
    return {
        "dataitems": [
            {
                "key": output,
                "kind": DATAITEM_DBT,
                "id": f"store://{dataitem.project}/dataitems/{dataitem.kind}/{dataitem.name}:{dataitem.id}",
            }
        ]
    }


####################
# Main
####################


def main() -> None:
    print("Initializing dbt project and running it...")

    # retrieve the run from core
    sdk.get_project(PROJECT_NAME)
    run: Run = sdk.get_run(PROJECT_NAME, RUN_ID)
    spec: RunSpec = run.spec

    # retrieve inputs and materialize
    inputs = spec.get_inputs().get("dataitems", [])
    materialize_inputs(inputs)

    outputs = spec.get_outputs().get("dataitems", ["output"])
    output = outputs[0]

    # generate uuid for dataitem
    uuid = str(uuid4())

    # retrieve model sql from run
    sql = run.spec.to_dict().get("dbt").get("sql")
    sql = base64.b64decode(sql).decode()

    # initialize dbt project, run dbt and inspect results
    initialize_dbt_project(sql, inputs, output, uuid)
    res = execute_dbt_project(output)

    print("======================= Parse results ========================")
    result: RunResult = parse_dbt_results(res, output)
    try:
        path = get_path(result)
        raw_code, compiled_code = get_code(result)
        timings = get_timings(result)
        name = result.node.name
    except Exception as e:
        raise RuntimeError("Something got wrong during object result access") from e

    print("======================= CREATE DATAITEM ========================")
    try:
        dataitem = sdk.new_dataitem(
            project=PROJECT_NAME,
            name=name,
            kind=DATAITEM_DBT,
            path=path,
            raw_code=raw_code,
            compiled_code=compiled_code,
            uuid=uuid,
        )
    except Exception as e:
        raise RuntimeError("Something got wrong during dataitem creation") from e

    dataitem_info = get_dataitem_info(output, dataitem)
    status_dict = {
        "status": {
            **dataitem_info,
            **timings,
        }
    }
    run = sdk.get_run(PROJECT_NAME, RUN_ID)
    print(run)
    run.set_status(status_dict)
    print("-----------------------")
    print(run)
    print("======================= UPDATE RUN ========================")
    try:
        sdk.update_run(run)
    except Exception as e:
        raise RuntimeError("Something got wrong during run update") from e

    # TODO: devo verificare che fqn=['default_name', 'output'], ho preso il progetto
    # giusto con il modello giusto.

    # se e' giusto passo lo status della run al backend (core) [status, timing]
    # ci interessa l'esito (success/error), metadata sull'esecuzione
    # (es execution time), tipo di output (es output)
    #       'adapter_response': {'_message': 'CREATE VIEW', 'code': 'CREATE VIEW',
    # 'rows_affected': -1},
    #       'message': 'CREATE VIEW',

    # del modello ci interessa il path come dataitem sql://postgres......
    # relation_name='"dbt"."public"."output"',
    # ci interessa inoltre il raw_code e il compiled_code ( va messo tutto in extra )


if __name__ == "__main__":
    main()
