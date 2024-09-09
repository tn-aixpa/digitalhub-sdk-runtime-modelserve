from __future__ import annotations

import typing
from typing import Any

from digitalhub_data.readers.registry import REGISTRY_DATAFRAME, REGISTRY_FRAMEWORK

if typing.TYPE_CHECKING:
    from digitalhub_data.readers.objects.base import DataframeReader


def get_reader_by_engine(engine: str) -> DataframeReader:
    """
    Get Dataframe reader.

    Parameters
    ----------
    engine : str
        Dataframe engine (pandas, polars, etc.).

    Returns
    -------
    DataframeReader
        Reader object.
    """
    try:
        return REGISTRY_FRAMEWORK[engine]()
    except KeyError:
        engines = list(REGISTRY_FRAMEWORK.keys())
        msg = f"Unsupported dataframe engine: {engine}. Supported engines: {engines}"
        raise ValueError(msg)


def get_reader_by_object(obj: Any) -> DataframeReader:
    """
    Get Dataframe reader by object.

    Parameters
    ----------
    obj : Any
        Object to get reader from.

    Returns
    -------
    DataframeReader
        Reader object.
    """
    try:
        obj_name = f"{obj.__class__.__module__}.{obj.__class__.__name__}"
        return REGISTRY_DATAFRAME[obj_name]()
    except KeyError:
        types = list(REGISTRY_DATAFRAME.keys())
        msg = f"Unsupported dataframe type: {obj}. Supported types: {types}"
        raise ValueError(msg)
