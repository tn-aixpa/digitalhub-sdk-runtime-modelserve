"""
Abstract entity module.
"""
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from sdk.entities.utils import file_exporter


class ModelObj:
    def to_dict(self) -> dict:
        """
        Return object as dict with all keys.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.

        """
        obj = {}
        for k in self.__dict__.keys():
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


@dataclass
class EntityMetadata(ModelObj):
    """
    A class representing the metadata of an entity.
    """

    name: str
    description: str = None

    @classmethod
    def from_dict(cls, obj: dict) -> "EntityMetadata":
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
        return cls(**obj)


@dataclass
class EntitySpec(ModelObj):
    """
    A class representing the specification of an entity.
    """

    @classmethod
    def from_dict(cls, obj: dict) -> "EntitySpec":
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


class Entity(ModelObj, metaclass=ABCMeta):
    """
    Abstract class for entities.
    """

    _obj_attr = ["name", "kind", "metadata", "spec", "project"]

    def __init__(self) -> None:
        self.id = None

    @abstractmethod
    def save(self, overwrite: bool = False) -> dict:
        ...

    @abstractmethod
    def export(self, filename: str = None) -> None:
        ...

    @staticmethod
    def export_object(filename: str, obj: dict) -> None:
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
            return file_exporter(filename, obj)
        except Exception as e:
            raise e

    def to_dict(self) -> dict:
        """
        Return object as dict with all keys.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.

        """
        d = super().to_dict()
        return {k: v for k, v in d.items() if k in self._obj_attr}

    def to_dict_not_embed(self) -> dict:
        return {
            k: v for k, v in self.__dict__.items() if k in ["project", "name", "kind"]
        }

    @classmethod
    @abstractmethod
    def from_dict(cls, *args, **kwargs) -> None:
        ...
