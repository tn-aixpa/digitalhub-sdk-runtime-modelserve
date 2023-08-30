"""
Task specification builder module.
"""
from __future__ import annotations

import typing

from sdk.entities.task.spec.build import TaskSpecBuild
from sdk.entities.task.spec.run import TaskSpecRun
from sdk.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from sdk.entities.task.spec.base import TaskSpec


REGISTRY = {
    "task": TaskSpecRun,
    "build": TaskSpecBuild,
}


def build_spec(kind: str, **kwargs) -> TaskSpec:
    """
    Build an TaskSpecJob object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of TaskSpec to build.
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    TaskSpec
        An TaskSpec object with the given parameters.

    Raises
    ------
    ValueError
        If the given kind is not supported.
    """
    try:
        return REGISTRY[kind](**kwargs)
    except KeyError:
        raise EntityError(f"Unsupported kind: {kind}")
