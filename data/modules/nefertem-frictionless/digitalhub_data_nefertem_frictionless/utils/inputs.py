"""
Runtime nefertem module.
"""
from __future__ import annotations

import typing

from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data.entities.dataitems.crud import get_dataitem

if typing.TYPE_CHECKING:
    from digitalhub_data.entities.dataitems.entity import Dataitem


def get_dataitem_(name: str, project: str) -> Dataitem:
    """
    Get dataitem from backend.

    Parameters
    ----------
    name : str
        The dataitem name.
    project : str
        The project name.

    Returns
    -------
    dict
        The dataitem.

    Raises
    ------
    BackendError
        If the dataitem cannot be retrieved.
    """
    try:
        LOGGER.info(f"Getting dataitem '{name}'.")
        return get_dataitem(project, name)
    except Exception:
        msg = f"Error getting dataitem '{name}'."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def persist_dataitem(dataitem: Dataitem, name: str, output_path: str) -> dict:
    """
    Persist dataitem locally.

    Parameters
    ----------
    dataitem : Dataitem
        The dataitem to persist.
    name : str
        The dataitem name.
    output_path : str
        The dataitem output path.

    Returns
    -------
    dict
        The dataitem path.

    Raises
    ------
    EntityError
        If the dataitem cannot be persisted.
    """
    try:
        LOGGER.info(f"Persisting dataitem '{name}' locally.")
        tmp_path = f"{output_path}/tmp/{name}.csv"
        dataitem.as_df().to_csv(tmp_path, sep=",", index=False)
        return {"name": name, "path": tmp_path}
    except Exception:
        msg = f"Error during dataitem '{name}' collection."
        LOGGER.exception(msg)
        raise EntityError(msg)
