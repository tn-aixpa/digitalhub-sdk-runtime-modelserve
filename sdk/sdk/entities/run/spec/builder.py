"""
Run specification builder module.
"""
from __future__ import annotations

import typing

from sdk.entities.base.spec import spec_builder
from sdk.entities.run.spec.registry import REGISTRY_MODEL, REGISTRY_SPEC

if typing.TYPE_CHECKING:
    from sdk.entities.run.spec.objects.base import RunSpec


def build_spec(kind: str, merged: bool = False, **kwargs) -> RunSpec:
    """
    Build an RunSpecJob object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of RunSpec to build.
    merged : bool
        If True, the given parameters will be merged with the default parameters.
    **kwargs
        Keywords arguments.

    Returns
    -------
    RunSpec
        An RunSpec object with the given parameters.

    Raises
    ------
    EntityError
        If the given kind is not supported.
    """
    ignore_validation = True if merged else False
    return spec_builder(
        kind, REGISTRY_SPEC, REGISTRY_MODEL, ignore_validation, **kwargs
    )
