"""
Model module.
"""
from __future__ import annotations

import typing

from sdk.context.builder import get_context
from sdk.entities.base.entity import Entity
from sdk.entities.builders.kinds import build_kind
from sdk.entities.builders.metadata import build_metadata
from sdk.entities.builders.spec import build_spec
from sdk.entities.builders.status import build_status
from sdk.utils.api import api_ctx_create, api_ctx_update
from sdk.utils.commons import MDLS
from sdk.utils.generic_utils import build_uuid, get_timestamp

if typing.TYPE_CHECKING:
    from sdk.context.context import Context
    from sdk.entities.models.metadata import ModelMetadata
    from sdk.entities.models.spec.objects.base import ModelSpec
    from sdk.entities.models.status import ModelStatus


class Model(Entity):
    """
    A class representing a model.
    """

    def __init__(
        self,
        uuid: str,
        kind: str,
        metadata: ModelMetadata,
        spec: ModelSpec,
        status: ModelStatus,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        uuid : str
            UUID.
        kind : str
            Kind of the object.
        metadata : ModelMetadata
            Metadata of the object.
        spec : ModelSpec
            Specification of the object.
        status : ModelStatus
            Status of the object.
        """
        super().__init__()
        self.id = uuid
        self.kind = kind
        self.metadata = metadata
        self.spec = spec
        self.status = status

        self.project = self.metadata.project
        self.name = self.metadata.name
        self.embedded = self.metadata.embedded
        self._obj_attr.extend(["project", "name", "embedded"])

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str | None = None) -> dict:
        """
        Save model into backend.

        Parameters
        ----------
        uuid : str
            UUID.

        Returns
        -------
        dict
            Mapping representation of Model from backend.
        """
        obj = self.to_dict()

        if uuid is None:
            api = api_ctx_create(self.metadata.project, MDLS)
            return self._context().create_object(obj, api)

        self.id = uuid
        self.metadata.updated = get_timestamp()
        obj["metadata"]["updated"] = self.metadata.updated
        api = api_ctx_update(self.metadata.project, MDLS, self.metadata.name, uuid)
        return self._context().update_object(obj, api)

    def export(self, filename: str | None = None) -> None:
        """
        Export object as a YAML file.

        Parameters
        ----------
        filename : str
            Name of the export YAML file. If not specified, the default value is used.

        Returns
        -------
        None
        """
        obj = self.to_dict()
        filename = filename if filename is not None else f"model_{self.metadata.project}_{self.metadata.name}.yaml"
        self._export_object(filename, obj)

    #############################
    #  Context
    #############################

    def _context(self) -> Context:
        """
        Get context.

        Returns
        -------
        Context
            Context.
        """
        return get_context(self.metadata.project)


def model_from_parameters(
    project: str,
    name: str,
    description: str | None = None,
    kind: str | None = None,
    embedded: bool = True,
    uuid: str | None = None,
    **kwargs,
) -> Model:
    """
    Create a new Model instance with the specified parameters.

    Parameters
    ----------
    project : str
        A string representing the project associated with this model.
    name : str
        The name of the model.
    description : str
        A description of the model.
    kind : str
        Kind of the object.
    embedded : bool
        Flag to determine if object must be embedded in project.
    uuid : str
        UUID.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Model
        An instance of the created model.
    """
    uuid = build_uuid(uuid)
    kind = build_kind(MDLS, kind)
    metadata = build_metadata(
        MDLS,
        project=project,
        name=name,
        version=uuid,
        description=description,
        embedded=embedded,
    )
    spec = build_spec(
        MDLS,
        kind,
        **kwargs,
    )
    status = build_status(MDLS)
    return Model(
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def model_from_dict(obj: dict) -> Model:
    """
    Create Model instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create Model from.

    Returns
    -------
    Model
        Model instance.
    """
    return Model.from_dict(MDLS, obj)
