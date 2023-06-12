"""
Abstract entity module.
"""
from abc import ABCMeta, abstractmethod

from sdk.utils.io_utils import file_exporter


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

    _obj_attr = ["name", "kind", "metadata", "spec", "project", "id", "embedded"]
    _essential_attr = ["project", "name", "kind", "embedded"]

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

    def to_dict_essential(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if k in self._essential_attr}

    @classmethod
    @abstractmethod
    def from_dict(cls, *args, **kwargs) -> None:
        ...
