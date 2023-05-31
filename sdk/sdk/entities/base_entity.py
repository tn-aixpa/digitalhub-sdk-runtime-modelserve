"""
Abstract entity module.
"""
from abc import ABCMeta, abstractmethod

from sdk.client.client import Client
from sdk.entities.utils import file_exporter


class Entity(metaclass=ABCMeta):
    """
    Abstract class for entities.
    """

    @abstractmethod
    def save(self, client: Client, overwrite: bool = False) -> dict:
        ...

    @abstractmethod
    def export(self, filename: str = None) -> None:
        ...

    @staticmethod
    def save_object(
        client: Client, obj: "Entity", api: str, overwrite: bool = False
    ) -> None:
        """
        Save entity into backend.

        Parameters
        ----------
        client : Client
            A client instance to store the entity.
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
        try:
            return client.create_object(obj, api)
        except KeyError:
            raise Exception("Object already present in the backend.")

    @staticmethod
    def export_object(filename: str, obj: "Entity") -> None:
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
        Return object to dict.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.

        """
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def __repr__(self) -> str:
        """
        Return string representation of the entity object.

        Returns
        -------
        str
            A string representing the entity instance.

        """
        return str(self.to_dict())
