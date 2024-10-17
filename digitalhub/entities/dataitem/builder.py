from __future__ import annotations

import typing

from digitalhub.factory.factory import factory
from digitalhub.utils.exceptions import BuilderError

if typing.TYPE_CHECKING:
    from digitalhub.entities.dataitem._base.entity import Dataitem


def dataitem_from_parameters(**kwargs) -> Dataitem:
    """
    Create a new object.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    Dataitem
        Object instance.
    """
    try:
        kind = kwargs["kind"]
    except KeyError:
        raise BuilderError("Missing 'kind' parameter.")
    return factory.build_entity_from_params(kind, **kwargs)


def dataitem_from_dict(obj: dict) -> Dataitem:
    """
    Create a new object from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    Dataitem
        Object instance.
    """
    try:
        kind = obj["kind"]
    except KeyError:
        raise BuilderError("Missing 'kind' parameter.")
    return factory.build_entity_from_dict(kind, obj)
