from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod

from digitalhub_core.entities._base.base import ModelObj

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.metadata import Metadata
    from digitalhub_core.entities._base.spec.base import Spec
    from digitalhub_core.entities._base.status.base import Status


class Entity(ModelObj, metaclass=ABCMeta):
    """
    Abstract class for entities.

    An entity is a collection of metadata, specification and status
    representing a variety of objects handled by Digitalhub.
    """

    # Entity type
    # Need to be set in subclasses
    ENTITY_TYPE: str

    # Attributes to render as dict. Need to be expanded in subclasses.
    _obj_attr = ["kind", "metadata", "spec", "status", "user", "key"]

    def __init__(
        self,
        kind: str,
        metadata: Metadata,
        spec: Spec,
        status: Status,
        user: str | None = None,
    ) -> None:
        self.kind = kind
        self.metadata = metadata
        self.spec = spec
        self.status = status
        self.user = user

        # Need to be set in subclasses
        self.key: str

    @abstractmethod
    def save(self, update: bool = False) -> Entity:
        """
        Abstract save method.
        """

    @abstractmethod
    def refresh(self) -> Entity:
        """
        Abstract refresh method.
        """

    def _update_attributes(self, obj: dict) -> None:
        """
        Update attributes.

        Parameters
        ----------
        obj : dict
            Mapping representation of object.

        Returns
        -------
        None
        """
        new_obj = self.from_dict(obj)
        self.metadata = new_obj.metadata
        self.spec = new_obj.spec
        self.status = new_obj.status
        self.user = new_obj.user

    @abstractmethod
    def export(self, filename: str | None = None) -> None:
        """
        Abstract export method.
        """

    def to_dict(self) -> dict:
        """
        Override default to_dict method to add the possibility to exclude
        some attributes. This requires to set a list of _obj_attr
        attributes in the subclass.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        return {k: v for k, v in super().to_dict().items() if k in self._obj_attr}

    @classmethod
    def from_dict(cls, obj: dict, validate: bool = True) -> Entity:
        """
        Create a new object from dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create object from.
        validate : bool
            Flag to indicate if arguments validation against a pydantic schema must be ignored.

        Returns
        -------
        Self
            Self instance.
        """
        parsed_dict = cls._parse_dict(obj, validate=validate)
        return cls(**parsed_dict)

    @staticmethod
    @abstractmethod
    def _parse_dict(obj: dict, validate: bool = True) -> dict:
        """
        Abstract method to parse dictionary.
        """

    def __repr__(self) -> str:
        """
        Return string representation of the entity object.

        Returns
        -------
        str
            A string representing the entity instance.
        """
        return str(self.to_dict())
