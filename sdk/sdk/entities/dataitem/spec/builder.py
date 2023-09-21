"""
Dataitem specification builder module.
"""
from __future__ import annotations

import typing

from sdk.entities.base.spec import spec_builder
from sdk.entities.dataitem.spec.registry import REGISTRY_MODEL, REGISTRY_SPEC

if typing.TYPE_CHECKING:
    from sdk.entities.dataitem.spec.objects.base import DataitemSpec


def build_spec(kind: str, **kwargs) -> DataitemSpec:
    """
    Build an DataitemSpecJob object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of DataitemSpec to build.
    **kwargs
        Keywords arguments.

    Returns
    -------
    DataitemSpec
        An DataitemSpec object with the given parameters.

    Raises
    ------
    EntityError
        If the given kind is not supported.
    """
    return spec_builder(kind, REGISTRY_SPEC, REGISTRY_MODEL, **kwargs)
