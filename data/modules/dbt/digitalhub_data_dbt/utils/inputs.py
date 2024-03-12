from __future__ import annotations

import typing

from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import decode_string
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data_dbt.utils.env import POSTGRES_DATABASE, POSTGRES_SCHEMA

if typing.TYPE_CHECKING:
    from digitalhub_data.entities.dataitems.entity._base import Dataitem


def materialize_dataitem(dataitem: Dataitem, name: str) -> str:
    """
    Materialize dataitem in postgres.

    Parameters
    ----------
    dataitem : Dataitem
        The dataitem.
    name : str
        The parameter SQL name.

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
        LOGGER.info(f"Materializing dataitem '{dataitem.name}' as '{table_name}'.")
        target_path = f"sql://{POSTGRES_DATABASE}/{POSTGRES_SCHEMA}/{table_name}"
        dataitem.write_df(target_path, if_exists="replace")
        return table_name
    except Exception:
        msg = f"Something got wrong during dataitem {name} materialization."
        LOGGER.exception(msg)
        raise EntityError(msg)


def decode_sql(sql: str) -> str:
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
        return decode_string(sql)
    except Exception:
        msg = "Sql code must be a valid string."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


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
