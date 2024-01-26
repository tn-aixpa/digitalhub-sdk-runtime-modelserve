from __future__ import annotations

from pathlib import Path

from digitalhub_data_dbt.utils.env import (
    POSTGRES_DATABASE,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_SCHEMA,
    POSTGRES_USER,
)

####################
# Templates
####################

PROJECT_TEMPLATE = """
name: "{}"
version: "1.0.0"
config-version: 2
profile: "postgres"
model-paths: ["{}"]
models:
""".lstrip(
    "\n"
)

MODEL_TEMPLATE_VERSION = """
models:
  - name: {}
    latest_version: {}
    versions:
        - v: {}
          config:
            materialized: table
""".lstrip(
    "\n"
)

PROFILE_TEMPLATE = f"""
postgres:
    outputs:
        dev:
            type: postgres
            host: {POSTGRES_HOST}
            user: {POSTGRES_USER}
            pass: {POSTGRES_PASSWORD}
            port: {POSTGRES_PORT}
            dbname: {POSTGRES_DATABASE}
            schema: {POSTGRES_SCHEMA}
    target: dev
""".lstrip(
    "\n"
)


def generate_dbt_profile_yml(root_dir: Path) -> None:
    """
    Create dbt profiles.yml

    Returns
    -------
    None
    """
    profiles_path = root_dir / "profiles.yml"
    profiles_path.write_text(PROFILE_TEMPLATE)


def generate_dbt_project_yml(root_dir: Path, model_dir: Path, project: str) -> None:
    """
    Create dbt_project.yml from 'dbt'

    Parameters
    ----------
    project : str
        The project name.

    Returns
    -------
    None
    """
    project_path = root_dir / "dbt_project.yml"
    project_path.write_text(PROJECT_TEMPLATE.format(project, model_dir.name))


def generate_outputs_conf(model_dir: Path, sql: str, output: str, uuid: str) -> None:
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
    sql_path = model_dir / f"{output}.sql"
    sql_path.write_text(sql)

    output_path = model_dir / f"{output}.yml"
    output_path.write_text(MODEL_TEMPLATE_VERSION.format(output, uuid, uuid))


def generate_inputs_conf(model_dir: Path, name: str, uuid: str) -> None:
    """
    Generate inputs confs dependencies for dbt project.

    Parameters
    ----------
    project : str
        The project name.
    inputs : list
        The list of inputs dataitems names.

    Returns
    -------
    None
    """
    # write schema and version detail for inputs versioning
    input_path = model_dir / f"{name}.yml"
    input_path.write_text(MODEL_TEMPLATE_VERSION.format(name, uuid, uuid))

    # write also sql select for the schema
    sql_path = model_dir / f"{name}_v{uuid}.sql"
    sql_path.write_text(f'SELECT * FROM "{name}_v{uuid}"')
