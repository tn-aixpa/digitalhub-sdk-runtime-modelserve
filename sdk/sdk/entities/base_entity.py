"""
Abstract entity module.
"""
from abc import ABCMeta, abstractmethod

from sdk.client.client import Client


class Entity(metaclass=ABCMeta):
    """
    Abstract class for entities.
    """

    @abstractmethod
    def save(self, client: Client, overwrite: bool = False) -> None:
        """
        Save entity into backend.

        Parameters
        ----------
        client : Client
            A client instance to store the entity.
        overwrite : bool, optional
            A boolean flag indicating whether to overwrite existing entities in the same location.
            Default is False.

        Returns
        -------
        None

        """

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
