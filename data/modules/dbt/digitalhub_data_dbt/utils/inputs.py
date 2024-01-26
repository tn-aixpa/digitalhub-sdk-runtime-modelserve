from __future__ import annotations

import typing

from digitalhub_core.entities.dataitems.crud import get_dataitem
from digitalhub_core.utils.exceptions import BackendError, EntityError
from digitalhub_core.utils.generic_utils import decode_string
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data_dbt.utils.env import POSTGRES_DATABASE, POSTGRES_SCHEMA

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.dataitems.entity import Dataitem


def get_dataitem_(name: str, project: str) -> Dataitem:
    """
    Get dataitem from core.

    Parameters
    ----------
    name : str
        The dataitem name.
    project : str
        The project name.

    Returns
    -------
    Dataitem
        The dataitem.

    Raises
    ------
    BackendError
        If dataitem is not found.
    """
    try:
        LOGGER.info(f"Getting dataitem '{name}'")
        return get_dataitem(project, name)
    except BackendError:
        msg = f"Dataitem {name} not found."
        LOGGER.exception(msg)
        raise BackendError(msg)


def materialize_dataitem(dataitem: Dataitem, name: str) -> str:
    """
    Materialize dataitem in postgres.

    Parameters
    ----------
    dataitem : Dataitem
        The dataitem.
    name : str
        The dataitem name.

    Returns
    -------
    str
        The materialized table name.

    Raises
    ------
    EntityError
        If something got wrong during dataitem materialization.
    """
    try:
        table_name = f"{name}_v{dataitem.id}"
        LOGGER.info(f"Materializing dataitem '{name}' as '{table_name}'.")
        target_path = f"sql://{POSTGRES_DATABASE}/{POSTGRES_SCHEMA}/{table_name}"
        dataitem.write_df(target_path, if_exists="replace")
        return table_name
    except Exception:
        msg = f"Something got wrong during dataitem {name} materialization."
        LOGGER.exception(msg)
        raise EntityError(msg)


def get_sql(spec: dict) -> str:
    """
    Get sql code from run spec.

    Parameters
    ----------
    spec : dict
        The run spec.

    Returns
    -------
    str
        The sql code.

    Raises
    ------
    RuntimeError
        If sql code is not a valid string.
    """
    try:
        return decode_string(spec.get("sql"))
    except Exception:
        msg = "Sql code must be a valid string."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def get_output_table_name(spec: dict) -> str:
    """
    Get output table name from run spec.

    Parameters
    ----------
    spec : dict
        Run spec dict.

    Returns
    -------
    str
        The output dataitem/table name.

    Raises
    ------
    RuntimeError
        If outputs are not a list of one dataitem.
    """
    outputs = spec.get("outputs", {}).get("dataitems", [])
    if not isinstance(outputs, list) or len(outputs) > 1:
        msg = "Outputs must be a list of exactly one dataitem."
        LOGGER.error(msg)
        raise RuntimeError(msg)
    return str(outputs[0])
