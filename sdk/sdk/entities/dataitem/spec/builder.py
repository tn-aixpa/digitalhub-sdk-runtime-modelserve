"""
Dataitem specification module.
"""
from __future__ import annotations

import typing

from sdk.entities.dataitem.spec.dbt import DBTDataitemSpec

if typing.TYPE_CHECKING:
    from sdk.entities.dataitem.spec.base import DataitemSpec


REGISTRY = {
    "dbt": DBTDataitemSpec,
    "sql": DBTDataitemSpec,
}


def build_spec(kind: str, **kwargs) -> DataitemSpec:
    """
    Build a DataItemSpec object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of DataItemSpec to build.
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    DataItemSpec
        A DataItemSpec object with the given parameters.

    Raises
    ------
    ValueError
        If the given kind is not supported.
    """
    try:
        return REGISTRY[kind](**kwargs)
    except KeyError:
        raise ValueError(f"Unknown kind: {kind}")
