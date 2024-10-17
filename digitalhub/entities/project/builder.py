from __future__ import annotations

import typing

from digitalhub.factory.factory import factory
from digitalhub.utils.exceptions import BuilderError

if typing.TYPE_CHECKING:
    from digitalhub.entities.project._base.entity import Project


def project_from_parameters(**kwargs) -> Project:
    """
    Create a new object.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    Project
        Object instance.
    """
    try:
        kind = kwargs["kind"]
    except KeyError:
        raise BuilderError("Missing 'kind' parameter.")
    return factory.build_entity_from_params(kind, **kwargs)


def project_from_dict(obj: dict) -> Project:
    """
    Create a new object from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    Project
        Object instance.
    """
    try:
        kind = obj["kind"]
    except KeyError:
        raise BuilderError("Missing 'kind' parameter.")
    return factory.build_entity_from_dict(kind, obj)
