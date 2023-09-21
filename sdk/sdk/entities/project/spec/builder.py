"""
Project specification builder module.
"""
from __future__ import annotations

import typing

from sdk.entities.base.spec import spec_builder
from sdk.entities.project.spec.registry import REGISTRY_MODEL, REGISTRY_SPEC

if typing.TYPE_CHECKING:
    from sdk.entities.project.spec.objects.base import ProjectSpec


def build_spec(kind: str, **kwargs) -> ProjectSpec:
    """
    Build an ProjectSpecJob object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of ProjectSpec to build.
    **kwargs
        Keywords arguments.

    Returns
    -------
    ProjectSpec
        An ProjectSpec object with the given parameters.

    Raises
    ------
    EntityError
        If the given kind is not supported.
    """
    return spec_builder(kind, REGISTRY_SPEC, REGISTRY_MODEL, **kwargs)
