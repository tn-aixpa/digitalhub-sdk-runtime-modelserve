"""
Abstract entity module.
"""
from abc import ABCMeta, abstractmethod
from typing import Self

from sdk.entities.base.base_model import ModelObj
from sdk.utils.io_utils import write_yaml


class Entity(ModelObj, metaclass=ABCMeta):
    """
    Abstract class for entities.
    """

    def __init__(self) -> None:
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
    def save(self, uuid: str | None = None) -> dict:
        """
        Abstract save method.
        """

    @abstractmethod
    def export(self, filename: str | None = None) -> None:
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
        return write_yaml(obj, filename)

    def to_dict(self, include_all_non_private: bool = False) -> dict:
        """
        Return object as dict with all keys.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        dict_ = super().to_dict()
        if include_all_non_private:
            return dict_
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
    def from_dict(cls, obj: dict) -> Self:
        """
        Abstract method for creating objects from a dictionary.
        """

    def __repr__(self) -> str:
        """
        Return string representation of the entity object.

        Returns
        -------
        str
            A string representing the entity instance.
        """
        return str(self.to_dict(include_all_non_private=True))
