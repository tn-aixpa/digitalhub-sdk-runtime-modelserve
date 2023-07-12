"""
Workflow module.
"""
from __future__ import annotations

import typing
from typing import Self

from sdk.entities.base.entity import Entity
from sdk.entities.workflow.metadata import build_metadata
from sdk.entities.workflow.spec import build_spec
from sdk.utils.api import DTO_WKFL, api_ctx_create, api_ctx_update
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context
from sdk.entities.utils.utils import get_uiid

if typing.TYPE_CHECKING:
    from sdk.entities.workflow.metadata import WorkflowMetadata
    from sdk.entities.workflow.spec import WorkflowSpec


class Workflow(Entity):
    """
    A class representing a workflow.
    """

    def __init__(
        self,
        project: str,
        name: str,
        kind: str = None,
        metadata: WorkflowMetadata = None,
        spec: WorkflowSpec = None,
        local: bool = False,
        embedded: bool = False,
        uuid: str = None,
        **kwargs,
    ) -> None:
        """
        Initialize the Workflow instance.

        Parameters
        ----------
        project : str
            Name of the project.
        name : str
            Name of the workflow.
        kind : str, optional
            Kind of the workflow, default is 'workflow'.
        metadata : WorkflowMetadata, optional
            Metadata for the workflow, default is None.
        spec : WorkflowSpec, optional
            Specification for the workflow, default is None.
        local: bool, optional
            Specify if run locally, default is False.
        embedded: bool, optional
            Specify if embedded, default is False.
        **kwargs
            Additional keyword arguments.
        """
        super().__init__()
        self.project = project
        self.name = name
        self.kind = kind if kind is not None else "local"
        self.metadata = (
            metadata if metadata is not None else WorkflowMetadata(name=name)
        )
        self.spec = spec if spec is not None else WorkflowSpec()
        self.embedded = embedded
        self.id = uuid if uuid is not None else get_uiid()

        self._local = local

        # Set new attributes
        self._any_setter(**kwargs)

        # Set context
        self._context = get_context(self.project)

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str = None) -> dict:
        """
        Save workflow into backend.

        Parameters
        ----------
        uuid : str, optional
            UUID of the workflow to update, default is None.

        Returns
        -------
        dict
            Mapping representation of Workflow from backend.

        """
        if self._local:
            raise EntityError("Use .export() for local execution.")

        obj = self.to_dict()

        if uuid is None:
            api = api_ctx_create(self.project, DTO_WKFL)
            return self._context.create_object(obj, api)

        self.id = uuid
        api = api_ctx_update(self.project, DTO_WKFL, self.name, uuid)
        return self._context.update_object(obj, api)

    def export(self, filename: str = None) -> None:
        """
        Export object as a YAML file.

        Parameters
        ----------
        filename : str, optional
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
        """
        return self._local

    #############################
    #  Generic Methods
    #############################

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        """
        Create object instance from a dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create object from.

        Returns
        -------
        Self
            Self instance.

        """
        parsed_dict = cls._parse_dict(obj)
        obj_ = cls(**parsed_dict)
        obj_._local = obj_._context.local
        return obj_

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
        embedded = obj.get("embedded")

        # Build metadata and spec
        spec = obj.get("spec")
        spec = spec if spec is not None else {}
        spec = build_spec(kind=kind, **spec)
        metadata = obj.get("metadata", {"name": name})
        metadata = build_metadata(**metadata)

        return {
            "project": project,
            "name": name,
            "kind": kind,
            "uuid": uuid,
            "metadata": metadata,
            "spec": spec,
            "embedded": embedded,
        }


def workflow_from_parameters(
    project: str,
    name: str,
    description: str = "",
    kind: str = "job",
    test: str = None,
    local: bool = False,
    embedded: bool = False,
    uuid: str = None,
) -> Workflow:
    """
    Create a new Workflow instance with the specified parameters.

    Parameters
    ----------
    project : str
        A string representing the project associated with this workflow.
    name : str
        The name of the workflow.
    description : str, optional
        A description of the workflow.
    kind : str, optional
        The kind of the workflow.
    spec : dict, optional
        The specification for the workflow.
    local : bool, optional
        Flag to determine if object has local execution.
    embedded : bool, optional
        Flag to determine if object must be embedded in project.
    uuid : str, optional
        The UUID.

    Returns
    -------
    Workflow
        An instance of the created workflow.

    """
    meta = build_metadata(name=name, description=description)
    spec = build_spec(kind, test=test)
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
