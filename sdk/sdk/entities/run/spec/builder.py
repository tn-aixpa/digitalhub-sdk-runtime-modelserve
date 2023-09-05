"""
Run specification module.
"""
from __future__ import annotations

import typing

from pydantic.errors import ValidationError

from sdk.entities.run.spec.base import RunSpec
from sdk.entities.run.spec.models import RunParams
from sdk.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from pydantic import BaseModel


REGISTRY_SPEC = {
    "run": RunSpec,
}
REGISTRY_MODEL = {
    "run": RunParams,
}


def build_spec(kind: str, **kwargs) -> RunSpec:
    """
    Build a RunSpecJob object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of RunSpec to build.
    **kwargs
        Keywords arguments.

    Returns
    -------
    RunSpec
        A RunSpec object with the given parameters.

    Raises
    ------
    EntityError
        If the given kind is not supported or if the given parameters are invalid.
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
