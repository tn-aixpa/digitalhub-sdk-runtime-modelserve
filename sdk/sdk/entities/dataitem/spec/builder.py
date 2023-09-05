"""
Dataitem specification module.
"""
from __future__ import annotations

import typing

from sdk.entities.dataitem.spec.table import TableDataitemSpec

if typing.TYPE_CHECKING:
    from sdk.entities.dataitem.spec.base import DataitemSpec


REGISTRY_SPEC = {
    "dataitem": TableDataitemSpec,
    "table": TableDataitemSpec,
}


def build_spec(kind: str, **kwargs) -> DataitemSpec:
    """
    Build a DataItemSpec object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of DataItemSpec to build.
    **kwargs
        Keywords arguments.

    Returns
    -------
    DataItemSpec
        A DataItemSpec object with the given parameters.

    Raises
    ------
    EntityError
        If the given kind is not supported.
    """
    try:
        return REGISTRY_SPEC[kind](**kwargs)
    except KeyError:
        raise ValueError(f"Unknown kind: {kind}")
