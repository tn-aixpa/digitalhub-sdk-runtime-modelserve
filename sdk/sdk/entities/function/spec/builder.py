"""
Function specification builder module.
"""
from __future__ import annotations

import typing

from sdk.entities.function.spec.dbt import FunctionSpecDBT
from sdk.entities.function.spec.job import FunctionSpecJob
from sdk.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from sdk.entities.function.spec.base import FunctionSpec


REGISTRY = {
    "job": FunctionSpecJob,
    "dbt": FunctionSpecDBT,
}


def build_spec(kind: str, **kwargs) -> FunctionSpec:
    """
    Build a FunctionSpecJob object with the given parameters.
    Kwargs are passed to the spec constructor.

    Parameters
    ----------
    kind : str
        The type of FunctionSpec to build.
    **kwargs : dict
        Keywords arguments.

    Returns
    -------
    FunctionSpec
        A FunctionSpec object with the given parameters.

    Raises
    ------
    EntityError
        If the given kind is not supported.
    """
    try:
        return REGISTRY[kind](**kwargs)
    except KeyError:
        raise EntityError(f"Unsupported kind: {kind}")
