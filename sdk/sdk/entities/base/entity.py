"""
Abstract entity module.
"""
from abc import ABCMeta, abstractmethod

from sdk.entities.base.base import ModelObj
from sdk.entities.builders.kinds import build_kind
from sdk.entities.builders.metadata import build_metadata
from sdk.entities.builders.spec import build_spec
from sdk.entities.builders.status import build_status
from sdk.utils.generic_utils import build_uuid
from sdk.utils.io_utils import write_yaml


class Entity(ModelObj, metaclass=ABCMeta):
    """
    Abstract class for entities.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        # Attributes to render as dict
        self._obj_attr = [
            "id",
            "kind",
            "metadata",
            "spec",
            "status",
        ]
        self._essential_attr = ["kind", "metadata"]

    @abstractmethod
    def save(self, update: bool = False) -> dict:
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

        Parameters
        ----------
        include_all_non_private : bool
            Whether to include all non-private attributes. If False, only
            attributes in the _obj_attr list will be included.

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
    def from_dict(cls, entity: str, obj: dict) -> "Entity":
        """
        Create object instance from a dictionary.

        Parameters
        ----------
        entity : str
            Entity type.
        obj : dict
            Dictionary to create object from.

        Returns
        -------
        Workflow
            Self instance.
        """
        parsed_dict = cls._parse_dict(entity, obj)
        return cls(**parsed_dict)

    @staticmethod
    def _parse_dict(entity: str, obj: dict) -> dict:
        """
        Get dictionary and parse it to a valid entity dictionary.

        Parameters
        ----------
        entity : str
            Entity type.
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        uuid = build_uuid(obj.get("id"))
        kind = build_kind(entity, obj.get("kind"))
        metadata = build_metadata(entity, **obj.get("metadata"))
        spec = build_spec(entity, kind, ignore_validation=True, **obj.get("spec"))
        status = build_status(entity, **obj.get("status"))
        return {
            "uuid": uuid,
            "kind": kind,
            "metadata": metadata,
            "spec": spec,
            "status": status,
        }

    def __repr__(self) -> str:
        """
        Return string representation of the entity object.

        Returns
        -------
        str
            A string representing the entity instance.
        """
        return str(self.to_dict(include_all_non_private=True))
