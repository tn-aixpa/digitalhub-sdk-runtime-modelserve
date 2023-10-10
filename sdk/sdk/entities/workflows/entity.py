"""
Workflow module.
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
from sdk.utils.commons import WKFL
from sdk.utils.exceptions import EntityError
from sdk.utils.generic_utils import build_uuid

if typing.TYPE_CHECKING:
    from sdk.context.context import Context
    from sdk.entities.workflows.metadata import WorkflowMetadata
    from sdk.entities.workflows.spec.objects.base import WorkflowSpec
    from sdk.entities.workflows.status import WorkflowStatus


class Workflow(Entity):
    """
    A class representing a workflow.
    """

    def __init__(
        self,
        uuid: str,
        kind: str,
        metadata: WorkflowMetadata,
        spec: WorkflowSpec,
        status: WorkflowStatus,
        local: bool = False,
    ) -> None:
        """
        Initialize the Workflow instance.

        Parameters
        ----------
        uuid : str
            UUID.
        kind : str
            Kind of the object.
        metadata : WorkflowMetadata
            Metadata of the object.
        spec : WorkflowSpec
            Specification of the object.
        status : WorkflowStatus
            State of the object.
        local: bool
            If True, export locally.
        """
        super().__init__()

        self.id = uuid
        self.kind = kind
        self.metadata = metadata
        self.spec = spec
        self.status = status

        # Private attributes
        self._local = local

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str | None = None) -> dict:
        """
        Save workflow into backend.

        Parameters
        ----------
        uuid : str
            UUID.

        Returns
        -------
        dict
            Mapping representation of Workflow from backend.
        """
        if self._local:
            raise EntityError("Use .export() for local execution.")

        obj = self.to_dict()

        # TODO: Remove this when backend is fixed
        obj["project"] = self.metadata.project
        obj["name"] = self.metadata.name
        obj["embedded"] = self.metadata.embedded

        if uuid is None:
            api = api_ctx_create(self.metadata.project, WKFL)
            return self._context().create_object(obj, api)

        self.id = uuid
        api = api_ctx_update(self.metadata.project, WKFL, self.metadata.name, uuid)
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
        filename = (
            filename
            if filename is not None
            else f"workflow_{self.metadata.project}_{self.metadata.name}.yaml"
        )
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

    #############################
    #  Generic Methods
    #############################

    @classmethod
    def from_dict(cls, obj: dict) -> "Workflow":
        """
        Create object instance from a dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create object from.

        Returns
        -------
        Workflow
            Self instance.
        """
        parsed_dict = cls._parse_dict(obj)
        _obj = cls(**parsed_dict)
        _obj._local = _obj._context().local
        return _obj

    @staticmethod
    def _parse_dict(obj: dict) -> dict:
        """
        Parse dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            Parsed dictionary.
        """

        # Mandatory fields
        project = obj.get("project")
        name = obj.get("name")
        if project is None or name is None:
            raise EntityError("Project or name are not specified.")

        # Build UUID, kind, metadata, spec and status
        uuid = obj.get("id")
        uuid = build_uuid(uuid)

        kind = obj.get("kind")
        kind = build_kind(WKFL, kind)

        metadata = obj.get("metadata")
        metadata = (
            metadata
            if metadata is not None
            else {"project": project, "name": name, "version": uuid}
        )
        metadata = build_metadata(WKFL, **metadata)

        spec = obj.get("spec")
        spec = spec if spec is not None else {}
        spec = build_spec(WKFL, kind=kind, **spec)

        status = obj.get("status")
        status = status if status is not None else {}
        status = build_status(WKFL, **status)

        return {
            "uuid": uuid,
            "kind": kind,
            "metadata": metadata,
            "spec": spec,
            "status": status,
        }


def workflow_from_parameters(
    project: str,
    name: str,
    description: str | None = None,
    kind: str | None = None,
    test: str | None = None,
    local: bool = False,
    embedded: bool = True,
    uuid: str | None = None,
    **kwargs,
) -> Workflow:
    """
    Create a new Workflow instance with the specified parameters.

    Parameters
    ----------
    project : str
        A string representing the project associated with this workflow.
    name : str
        The name of the workflow.
    description : str
        A description of the workflow.
    kind : str
        Kind of the object.
    spec : dict
        Specification of the object.
    local : bool
        Flag to determine if object will be exported to backend.
    embedded : bool
        Flag to determine if object must be embedded in project.
    uuid : str
        UUID.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Workflow
        An instance of the created workflow.
    """
    uuid = build_uuid(uuid)
    kind = build_kind(WKFL, kind)
    metadata = build_metadata(
        WKFL,
        project=project,
        name=name,
        version=uuid,
        description=description,
        embedded=embedded,
    )
    spec = build_spec(
        WKFL,
        kind,
        test=test,
        **kwargs,
    )
    status = build_status(WKFL)
    return Workflow(
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
        local=local,
    )


def workflow_from_dict(obj: dict) -> Workflow:
    """
    Create Workflow instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create Workflow from.

    Returns
    -------
    Workflow
        Workflow instance.
    """
    return Workflow.from_dict(obj)
