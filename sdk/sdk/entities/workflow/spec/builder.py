"""
Workflow specification builder module.
"""
from __future__ import annotations

import typing

from sdk.entities.base.spec import spec_builder
from sdk.entities.workflow.spec.registry import REGISTRY_MODEL, REGISTRY_SPEC

if typing.TYPE_CHECKING:
    from sdk.entities.workflow.spec.objects.base import WorkflowSpec


def build_spec(kind: str, **kwargs) -> WorkflowSpec:
    """
    Build an WorkflowSpecJob object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of WorkflowSpec to build.
    **kwargs
        Keywords arguments.

    Returns
    -------
    WorkflowSpec
        An WorkflowSpec object with the given parameters.

    Raises
    ------
    EntityError
        If the given kind is not supported.
    """
    return spec_builder(kind, REGISTRY_SPEC, REGISTRY_MODEL, **kwargs)
