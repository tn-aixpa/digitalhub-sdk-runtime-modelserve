from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod

from digitalhub.entities._builders.metadata import build_metadata
from digitalhub.entities._builders.name import build_name
from digitalhub.entities._builders.spec import build_spec
from digitalhub.entities._builders.status import build_status
from digitalhub.entities._builders.uuid import build_uuid

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.entity import Entity
    from digitalhub.entities._base.entity.metadata import Metadata
    from digitalhub.entities._base.entity.spec import Spec, SpecValidator
    from digitalhub.entities._base.entity.status import Status


class EntityBuilder(metaclass=ABCMeta):
    """
    Builder class for building entities.
    """

    # Class variables
    ENTITY_CLASS: Entity = None
    ENTITY_SPEC_CLASS: Spec = None
    ENTITY_SPEC_VALIDATOR: SpecValidator = None
    ENTITY_STATUS_CLASS: Status = None

    def __init__(self) -> None:
        if self.ENTITY_CLASS is None:
            raise ValueError("ENTITY_CLASS must be set")
        if self.ENTITY_SPEC_CLASS is None:
            raise ValueError("ENTITY_SPEC_CLASS must be set")
        if self.ENTITY_SPEC_VALIDATOR is None:
            raise ValueError("ENTITY_SPEC_VALIDATOR must be set")
        if self.ENTITY_STATUS_CLASS is None:
            raise ValueError("ENTITY_STATUS_CLASS must be set")

    def build_name(self, name: str) -> str:
        """
        Build entity name.

        Parameters
        ----------
        name : str
            Entity name.

        Returns
        -------
        str
            Entity name.
        """
        return build_name(name)

    def build_uuid(self, uuid: str) -> str:
        """
        Build entity uuid.

        Parameters
        ----------
        uuid : str
            Entity uuid.

        Returns
        -------
        str
            Entity uuid.
        """
        return build_uuid(uuid)

    def build_metadata(self, kind: str, **kwargs) -> Metadata:
        """
        Build entity metadata object.

        Parameters
        ----------
        kind : str
            Registry entry kind.
        **kwargs : dict
            Keyword arguments for the constructor.

        Returns
        -------
        Metadata
            Metadata object.
        """
        return build_metadata(kind, **kwargs)

    def build_spec(self, kind: str, **kwargs) -> Spec:
        """
        Build entity spec object.

        Parameters
        ----------
        kind : str
            Registry entry kind.
        **kwargs : dict
            Keyword arguments for the constructor.

        Returns
        -------
        Spec
            Spec object.
        """
        return build_spec(kind, **kwargs)

    def build_status(self, kind: str, **kwargs) -> Status:
        """
        Build entity status object.

        Parameters
        ----------
        kind : str
            Registry entry kind.
        **kwargs : dict
            Keyword arguments for the constructor.

        Returns
        -------
        Status
            Status object.
        """
        return build_status(kind, **kwargs)

    @abstractmethod
    def build(self, _validate: bool = True, **kwargs) -> Entity:
        """
        Build entity object.
        """

    def from_dict(self, obj: dict, validate: bool = True) -> Entity:
        """
        Build entity from dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to build the entity from.
        validate : bool
            Whether to validate the entity.

        Returns
        -------
        ArtifactArtifact
            Entity built from the dictionary.
        """
        return self.build(**obj, _validate=validate)
