"""
Entity specification module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.base import ModelObj
from pydantic import BaseModel


class Spec(ModelObj):
    """
    A class representing the specification of an entity.
    """

    @classmethod
    def from_dict(cls, obj: dict) -> "Spec":
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
        return cls(**obj)


class SpecRegistry(dict):
    """
    Specification registry generic class.
    """

    def register(self, kind: str, spec: Spec, model: BaseModel) -> None:
        """
        Register for object specification.

        Parameters
        ----------
        kind : Enum
            Object kind.
        spec : Spec
            Object specification.
        model : BaseModel
            Object model.

        Returns
        -------
        None
        """
        self[kind] = {"spec": spec, "model": model}
