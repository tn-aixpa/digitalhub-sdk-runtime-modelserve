from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import requests
from digitalhub_core.utils.generic_utils import decode_string
from digitalhub_core.utils.logger import LOGGER
from digitalhub_core.utils.uri_utils import map_uri_scheme
from digitalhub_data_dbt.utils.env import (
    POSTGRES_DATABASE,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_SCHEMA,
    POSTGRES_USER,
)
from git import Repo

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


def get_output_table_name(outputs: list[dict]) -> str:
    """
    Get output table name from run spec.

    Parameters
    ----------
    outputs : list
        The outputs.

    Returns
    -------
    str
        The output dataitem/table name.

    Raises
    ------
    RuntimeError
        If outputs are not a list of one dataitem.
    """
    try:
        return outputs[0]["output_table"]
    except IndexError:
        msg = "Outputs must be a list of one dataitem."
        LOGGER.exception(msg)
        raise RuntimeError(msg)
    except KeyError:
        msg = "Must pass reference to 'output_table'."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def save_function_source(path: Path, source_spec: dict) -> str:
    """
    Save function source.

    Parameters
    ----------
    path : Path
        Path where to save the function source.
    source_spec : dict
        Function source spec.

    Returns
    -------
    path
        Path to the function source.
    """
    # Prepare path
    path.mkdir(parents=True, exist_ok=True)

    # First check if source is base64
    base64 = source_spec.get("base64")
    if base64 is not None:
        return decode_base64(base64)

    # Second check if source is path
    source = source_spec.get("source")
    if source is not None:
        scheme = map_uri_scheme(source)

        # Local paths are not supported
        if scheme == "local":
            raise RuntimeError("Local files are not supported at Runtime execution.")

        # Http(s) and remote paths (s3 presigned urls)
        if scheme == "remote":
            return get_remote_source(path, source)

        # Git repos
        if scheme == "git":
            return get_repository(path, source)

    raise RuntimeError("Function source not found.")


def get_remote_source(path: Path, source: str) -> str:
    """
    Get remote source.

    Parameters
    ----------
    source : str
        Source.

    Returns
    -------
    str
        Source.
    """
    try:
        filename = path / "archive.zip"
        with requests.get(source, stream=True) as r:
            r.raise_for_status()
            with filename.open("wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        with ZipFile(filename, "r") as zip_file:
            zip_file.extractall(path)
        return str(path)
    except Exception:
        msg = "Source must be a valid zipfile."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def get_repository(path: Path, source: str) -> str:
    """
    Get repository.

    Parameters
    ----------
    source : str
        Source.

    Returns
    -------
    str
        Repository.
    """
    try:
        source = source.replace("git://", "https://")
        path = path / "repository"
        Repo.clone_from(source, path)
        return str(path)
    except Exception:
        msg = "Source must be a valid url."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def decode_base64(base64: str) -> str:
    """
    Decode sql code.

    Parameters
    ----------
    sql : str
        The sql code.

    Returns
    -------
    str
        The decoded sql code.

    Raises
    ------
    RuntimeError
        If sql code is not a valid string.
    """
    try:
        return decode_string(base64)
    except Exception:
        msg = "Sql code must be a valid string."
        LOGGER.exception(msg)
        raise RuntimeError(msg)
