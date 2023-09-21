"""
Task specification builder module.
"""
from __future__ import annotations

import typing

from sdk.entities.base.spec import spec_builder
from sdk.entities.task.spec.registry import REGISTRY_MODEL, REGISTRY_SPEC

if typing.TYPE_CHECKING:
    from sdk.entities.task.spec.objects.base import TaskSpec


def build_spec(kind: str, **kwargs) -> TaskSpec:
    """
    Build an TaskSpecJob object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of TaskSpec to build.
    **kwargs
        Keywords arguments.

    Returns
    -------
    TaskSpec
        An TaskSpec object with the given parameters.

    Raises
    ------
    EntityError
        If the given kind is not supported.
    """
    return spec_builder(kind, REGISTRY_SPEC, REGISTRY_MODEL, **kwargs)
