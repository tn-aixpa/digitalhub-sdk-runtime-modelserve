"""
Abstract entity module.
"""
from abc import ABCMeta, abstractmethod
from typing import Any

from sdk.utils.io_utils import write_yaml


class ModelObj:
    """
    Base entity model.
    """

    def to_dict(self) -> dict:
        """
        Return object as dict with all keys.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.

        """
        obj = {}
        for k in self.__dict__:
            if k.startswith("_"):
                continue
            val = getattr(self, k, None)
            if val is not None:
                if hasattr(val, "to_dict"):
                    val = val.to_dict()
                    if val:
                        obj[k] = val
                else:
                    obj[k] = val
        return obj

    def __repr__(self) -> str:
        """
        Return string representation of the entity object.

        Returns
        -------
        str
            A string representing the entity instance.

        """
        return str(self.to_dict())


class EntityMetadata(ModelObj):
    """
    A class representing the metadata of an entity.
    """

    def __init__(self, name: str, description: str = None) -> None:
        self.name = name
        self.description = description

    @classmethod
    def from_dict(cls, obj: dict = None) -> "EntityMetadata":
        """
        Return entity metadata object from dictionary.

        Parameters
        ----------
        obj : dict
            A dictionary containing the attributes of the entity metadata.

        Returns
        -------
        EntityMetadata
            An entity metadata object.

        """
        if obj is None:
            obj = {}
        return cls(**obj)


class EntitySpec(ModelObj):
    """
    A class representing the specification of an entity.
    """

    @classmethod
    def from_dict(cls, obj: dict = None) -> "EntitySpec":
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
        if obj is None:
            obj = {}
        return cls(**obj)


class Entity(ModelObj, metaclass=ABCMeta):
    """
    Abstract class for entities.
    """

    def __init__(self) -> None:
        self.id = None
        self._obj_attr = [
            "id",
            "name",
            "kind",
            "metadata",
            "spec",
            "project",
            "embedded",
        ]
        self._essential_attr = ["name", "kind"]

    @abstractmethod
    def save(self, uuid: bool = False) -> dict:
        """
        Abstract save method.
        """

    @abstractmethod
    def export(self, filename: str = None) -> None:
        """
        Abstract save method.
        """

    @staticmethod
    def _export_object(filename: str, obj: dict) -> None:
        """
        Export object to a file in the specified filename location.

        Parameters
        ----------
        filename : str
            The absolute or relative path to the file in which the object
            will be exported.

        Returns
        -------
        None
        """
        try:
            return write_yaml(obj, filename)
        except Exception as exc:
            raise exc

    def to_dict(self) -> dict:
        """
        Return object as dict with all keys.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.

        """
        dict_ = super().to_dict()
        return {k: v for k, v in dict_.items() if k in self._obj_attr}

    def to_dict_essential(self) -> dict:
        """
        Return object as dict with some attributes.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.

        """
        dict_ = super().to_dict()
        return {k: v for k, v in dict_.items() if k in self._essential_attr}

    @classmethod
    @abstractmethod
    def from_dict(cls, obj: dict) -> Any:
        """
        Abstract method for creating objects from a dictionary.
        """
