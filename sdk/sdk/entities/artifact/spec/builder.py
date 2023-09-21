"""
Artifact specification builder module.
"""
from __future__ import annotations

import typing

from sdk.entities.artifact.spec.registry import REGISTRY_MODEL, REGISTRY_SPEC
from sdk.entities.base.spec import spec_builder

if typing.TYPE_CHECKING:
    from sdk.entities.artifact.spec.objects.base import ArtifactSpec


def build_spec(kind: str, **kwargs) -> ArtifactSpec:
    """
    Build an ArtifactSpecJob object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of ArtifactSpec to build.
    **kwargs
        Keywords arguments.

    Returns
    -------
    ArtifactSpec
        An ArtifactSpec object with the given parameters.

    Raises
    ------
    EntityError
        If the given kind is not supported.
    """
    return spec_builder(kind, REGISTRY_SPEC, REGISTRY_MODEL, **kwargs)
