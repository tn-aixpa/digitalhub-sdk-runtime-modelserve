"""
Abstract entity module.
"""
from abc import ABCMeta, abstractmethod

from pydantic import BaseModel

from sdk.client.client import Client
from sdk.client.factory import get_client
from sdk.entities.utils import file_exporter

from dataclasses import dataclass


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


@dataclass
class EntitySpec(ModelObj):
    """
    A class representing the specification of an entity.
    """


class Entity(ModelObj, metaclass=ABCMeta):
    """
    Abstract class for entities.
    """

    def __init__(self) -> None:
        self.id = None
        self._obj_attr = ["name", "kind", "metadata", "spec"]
        self._client = get_client()

    @abstractmethod
    def save(self, overwrite: bool = False) -> dict:
        ...

    @abstractmethod
    def export(self, filename: str = None) -> None:
        ...

    def save_object(
        self,
        obj: "Entity",
        api: str,
        overwrite: bool = False,
    ) -> None:
        """
        Save entity into backend.

        Parameters
        ----------
        obj : Entity
            Entity object to save.
        api : str
            Endpoint to call.
        overwrite : bool, optional
            A boolean flag indicating whether to overwrite existing entities in the same location.
            Default is False.

        Returns
        -------
        None

        """
        return self._client.create_object(obj, api)

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

    def to_dict_not_embed(self) -> dict:
        return {
            k: v for k, v in self.__dict__.items() if k in ["project", "name", "kind"]
        }

    def to_dict_complete(self) -> dict:
        """
        Return object as dict with all keys.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.

        """
        return {k: v for k, v in self.__dict__.items()}
