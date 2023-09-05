"""
Task specification builder module.
"""
from __future__ import annotations

import typing

from pydantic.errors import ValidationError

from sdk.entities.task.spec.build import TaskSpecBuild
from sdk.entities.task.spec.models import TaskTaskParams
from sdk.entities.task.spec.run import TaskSpecRun
from sdk.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from pydantic import BaseModel
    from sdk.entities.task.spec.base import TaskSpec


REGISTRY_SPEC = {
    "task": TaskSpecRun,
    "build": TaskSpecBuild,
}
REGISTRY_MODEL = {
    "task": TaskTaskParams,
}


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
    # First build the arguments model and validate them ...
    try:
        model: BaseModel = REGISTRY_MODEL[kind](**kwargs)
    except KeyError:
        raise EntityError(f"Unsupported parameters kind: {kind}")
    except ValidationError:
        raise EntityError(f"Invalid parameters for kind: {kind}")

    # ... then build the spec
    try:
        return REGISTRY_SPEC[kind](**model.model_dump())
    except KeyError:
        raise EntityError(f"Unsupported spec kind: {kind}")
