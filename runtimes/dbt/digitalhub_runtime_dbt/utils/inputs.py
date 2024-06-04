from __future__ import annotations

import typing

from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.logger import LOGGER
from digitalhub_runtime_dbt.utils.env import POSTGRES_DATABASE, POSTGRES_SCHEMA

if typing.TYPE_CHECKING:
    from digitalhub_data.entities.dataitems.entity.table import DataitemTable


def materialize_dataitem(dataitem: DataitemTable, name: str) -> str:
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
    except Exception as e:
        msg = f"Something got wrong during dataitem {name} materialization. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise EntityError(msg) from e
