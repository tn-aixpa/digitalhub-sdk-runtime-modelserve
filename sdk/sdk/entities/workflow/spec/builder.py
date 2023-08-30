"""
Workflow specification builder module.
"""
from __future__ import annotations

import typing

from sdk.entities.workflow.spec.job import WorkflowSpecJob
from sdk.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from sdk.entities.workflow.spec.base import WorkflowSpec


REGISTRY = {
    "job": WorkflowSpecJob,
}


def build_spec(kind: str, **kwargs) -> WorkflowSpec:
    """
    Build an WorkflowSpecJob object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of WorkflowSpec to build.
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    WorkflowSpec
        An WorkflowSpec object with the given parameters.

    Raises
    ------
    ValueError
        If the given kind is not supported.
    """
    try:
        return REGISTRY[kind](**kwargs)
    except KeyError:
        raise EntityError(f"Unsupported kind: {kind}")
