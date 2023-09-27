"""
Workflow module.
"""
from __future__ import annotations

import typing

from sdk.context.factory import get_context
from sdk.entities.base.entity import Entity
from sdk.entities.builders.kinds import build_kind
from sdk.entities.builders.metadata import build_metadata
from sdk.entities.builders.spec import build_spec
from sdk.entities.builders.status import build_status
from sdk.utils.api import api_ctx_create, api_ctx_update
from sdk.utils.commons import WKFL
from sdk.utils.exceptions import EntityError
from sdk.utils.generic_utils import get_uiid

if typing.TYPE_CHECKING:
    from sdk.entities.base.metadata import Metadata
    from sdk.entities.base.status import Status
    from sdk.entities.workflow.spec.objects.base import WorkflowSpec


class Workflow(Entity):
    """
    A class representing a workflow.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str | None = None,
        kind: str | None = None,
        metadata: Metadata | None = None,
        spec: WorkflowSpec | None = None,
        status: Status | None = None,
        local: bool = False,
        embedded: bool = True,
    ) -> None:
        """
        Initialize the Workflow instance.

        Parameters
        ----------
        project : str
            Name of the project.
        name : str
            Name of the object.
        uuid : str
            UUID.
        kind : str
            Kind of the object.
        metadata : Metadata
            Metadata of the object.
        spec : WorkflowSpec
            Specification of the object.
        status : Status
            State of the object.
        local: bool
            If True, export locally.
        embedded: bool
            If True, embed object in backend.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.id = get_uiid(uuid=uuid)
        self.kind = kind if kind is not None else build_kind(WKFL)
        self.metadata = metadata if metadata is not None else build_metadata(name=name)
        self.spec = spec if spec is not None else build_spec(WKFL, self.kind, **{})
        self.status = status if status is not None else build_status()
        self.embedded = embedded

        # Private attributes
        self._local = local
        self._context = get_context(self.project)

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

        if uuid is None:
            api = api_ctx_create(self.project, WKFL)
            return self._context.create_object(obj, api)

        self.id = uuid
        api = api_ctx_update(self.project, WKFL, self.name, uuid)
        return self._context.update_object(obj, api)

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
            else f"workflow_{self.project}_{self.name}.yaml"
        )
        self._export_object(filename, obj)

    #############################
    #  Workflow Methods
    #############################

    #############################
    #  Getters and Setters
    #############################

    @property
    def local(self) -> bool:
        """
        Get local flag.

        Returns
        -------
        bool
            Local flag.
        """
        return self._local

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
        _obj._local = _obj._context.local
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

        # Optional fields
        uuid = obj.get("id")
        kind = obj.get("kind")
        kind = build_kind(WKFL, kind)
        embedded = obj.get("embedded")

        # Build metadata, spec, status
        spec = obj.get("spec")
        spec = spec if spec is not None else {}
        spec = build_spec(WKFL, kind=kind, **spec)
        metadata = obj.get("metadata", {"name": name})
        metadata = build_metadata(**metadata)
        status = obj.get("status")
        status = status if status is not None else {}
        status = build_status(**status)

        return {
            "project": project,
            "name": name,
            "kind": kind,
            "uuid": uuid,
            "metadata": metadata,
            "spec": spec,
            "status": status,
            "embedded": embedded,
        }


def workflow_from_parameters(
    project: str,
    name: str,
    description: str = "",
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
    kind = build_kind(WKFL, kind)
    spec = build_spec(WKFL, kind, test=test, **kwargs)
    meta = build_metadata(name=name, description=description)
    return Workflow(
        project=project,
        name=name,
        kind=kind,
        metadata=meta,
        spec=spec,
        local=local,
        embedded=embedded,
        uuid=uuid,
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
