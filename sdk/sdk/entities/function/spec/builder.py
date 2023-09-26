"""
Function specification builder module.
"""
from __future__ import annotations

import typing

from sdk.entities.base.spec import spec_builder
from sdk.entities.function.spec.registry import REGISTRY_MODEL, REGISTRY_SPEC

if typing.TYPE_CHECKING:
    from sdk.entities.function.spec.objects.base import FunctionSpec


def build_spec(kind: str, **kwargs) -> FunctionSpec:
    """
    Build an FunctionSpec object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of FunctionSpec to build.
    **kwargs
        Keywords arguments.

    Returns
    -------
    FunctionSpec
        An FunctionSpec object with the given parameters.

    Raises
    ------
    EntityError
        If the given kind is not supported.
    """
    return spec_builder(kind, REGISTRY_SPEC, REGISTRY_MODEL, **kwargs)
