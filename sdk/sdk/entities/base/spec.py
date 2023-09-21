"""
Entity specification module.
"""
from __future__ import annotations

import typing

from pydantic import ValidationError

from sdk.entities.base.base_model import ModelObj
from sdk.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from pydantic import BaseModel


class EntitySpec(ModelObj):
    """
    A class representing the specification of an entity.
    """

    @classmethod
    def from_dict(cls, obj: dict | None = None) -> "EntitySpec":
        """
        Return entity specification object from dictionary.

        Parameters
        ----------
        obj : dict
            A dictionary containing the attributes of the entity specification.

        Returns
        -------
        EntitySpec
            An entity specification object.
        """
        obj = obj if obj is not None else {}
        return cls(**obj)


def spec_builder(
    kind: str, registry_spec: dict, registry_models: dict | None = None, **kwargs
) -> EntitySpec:
    """
    Build an Spec object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of Spec to build.
    registry_spec : dict
        The registry of Spec objects.
    registry_models : dict
        The registry of Model objects.

    Returns
    -------
    EntitySpec
        An Spec object with the given parameters.
    """

    params = validate_params(kind, registry_models, **kwargs)
    try:
        return registry_spec[kind](**params)
    except KeyError:
        raise EntityError(f"Unsupported spec kind: {kind}")


def validate_params(kind: str, registry_models: dict | None = None, **kwargs) -> dict:
    """
    Validate the parameters for the given kind of object.

    Parameters
    ----------
    kind : str
        The kind of the object.
    registry_models : dict
        The registry of Model objects.
    kwargs : dict
        The parameters to validate.

    Returns
    -------
    dict
        The validated parameters.
    """
    try:
        model: BaseModel = registry_models[kind](**kwargs)
        return model.model_dump()
    except KeyError:
        return kwargs
        raise EntityError(f"Unsupported parameters kind: {kind}")
    except ValidationError as ve:
        return kwargs
        raise EntityError(f"Invalid parameters for kind: {kind}") from ve
