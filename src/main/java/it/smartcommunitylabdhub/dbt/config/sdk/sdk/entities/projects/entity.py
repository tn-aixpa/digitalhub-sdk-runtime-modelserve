"""
Project module.
"""
from __future__ import annotations

import typing
from typing import Callable, TypeVar

from sdk.client.builder import get_client
from sdk.context.builder import set_context
from sdk.entities.artifacts.crud import (
    create_artifact_from_dict,
    delete_artifact,
    get_artifact,
    new_artifact,
)
from sdk.entities.base.entity import Entity
from sdk.entities.builders.kinds import build_kind
from sdk.entities.builders.metadata import build_metadata
from sdk.entities.builders.spec import build_spec
from sdk.entities.builders.status import build_status
from sdk.entities.dataitems.crud import (
    create_dataitem_from_dict,
    delete_dataitem,
    get_dataitem,
    new_dataitem,
)
from sdk.entities.functions.crud import (
    create_function_from_dict,
    delete_function,
    get_function,
    new_function,
)
from sdk.entities.workflows.crud import (
    create_workflow_from_dict,
    delete_workflow,
    get_workflow,
    new_workflow,
)
from sdk.utils.api import api_base_create
from sdk.utils.commons import ARTF, DTIT, FUNC, PROJ, WKFL
from sdk.utils.exceptions import BackendError, EntityError
from sdk.utils.generic_utils import build_uuid

if typing.TYPE_CHECKING:
    from sdk.client.client import Client
    from sdk.entities.artifacts.entity import Artifact
    from sdk.entities.dataitems.entity import Dataitem
    from sdk.entities.functions.entity import Function
    from sdk.entities.projects.metadata import ProjectMetadata
    from sdk.entities.projects.spec.objects.base import ProjectSpec
    from sdk.entities.projects.status import ProjectStatus
    from sdk.entities.workflows.entity import Workflow

    Entities = TypeVar("Entities", Artifact, Function, Workflow, Dataitem)


LIST = [ARTF, FUNC, WKFL, DTIT]
SPEC_LIST = LIST + ["source", "context"]


def constructor_from_dict(
    dto: str,
) -> Callable[[dict], Artifact | Function | Workflow | Dataitem]:
    """
    Get constructor for dto.

    Parameters
    ----------
    dto : str
        DTO.

    Returns
    -------
    Callable[[dict], Artifact | Function | Workflow | Dataitem]
        Constructor from dict.

    Raises
    ------
    EntityError
        If dto is not valid.
    """
    if dto == ARTF:
        return create_artifact_from_dict
    if dto == FUNC:
        return create_function_from_dict
    if dto == WKFL:
        return create_workflow_from_dict
    if dto == DTIT:
        return create_dataitem_from_dict
    raise EntityError(f"DTO {dto} is not valid.")


class Project(Entity):
    """
    A class representing a project.
    """

    def __init__(
        self,
        uuid: str,
        kind: str,
        metadata: ProjectMetadata,
        spec: ProjectSpec,
        status: ProjectStatus,
        local: bool = False,
    ) -> None:
        """
        Initialize the Project instance.

        Parameters
        ----------
        uuid : str
            UUID.
        kind : str
            Kind of the object.
        metadata : ProjectMetadata
            Metadata of the object.
        spec : ProjectSpec
            Specification of the object.
        status : ProjectStatus
            Status of the object.
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
        self._client = get_client() if not self.local else None

        # Set context
        set_context(self)

    #############################
    #  Save / Export
    #############################

    def save(self, uuid: str | None = None) -> dict:
        """
        Save project and context into backend.

        Parameters
        ----------
        uuid : bool
            Ignored, placed for compatibility with other objects.

        Returns
        -------
        list
            Mapping representation of Project from backend.
        """
        responses: dict = {}
        if self.local:
            raise EntityError("Use .export() for local execution.")

        obj = self.to_dict()

        # TODO: Remove this when backend is fixed
        obj["name"] = self.metadata.name

        # Try to create project
        # (try to avoid error response if project already exists)
        try:
            api = api_base_create(PROJ)
            response = self.client.create_object(obj, api)
            responses[PROJ] = response
        except BackendError:
            responses[PROJ] = obj

        # Try to save objects related to project
        # (try to avoid error response if object does not exists)
        for i in LIST:
            responses[i] = []
            for j in self._get_objects(i):
                try:
                    _obj = constructor_from_dict(i)(j)
                    resp = _obj.save(uuid=_obj.id)
                    responses[i].append(resp)
                except BackendError:
                    ...

        return responses

    def export(self, filename: str | None = None) -> None:
        """
        Export object as a YAML file. If the objects are not embedded, the objects are
        exported as a YAML file.

        Parameters
        ----------
        filename : str
            Name of the export YAML file. If not specified, the default value is used.

        Returns
        -------
        None
        """
        obj = self.to_dict()
        obj = self._parse_spec(obj)

        filename = filename if filename is not None else "project.yaml"
        self._export_object(filename, obj)

        # Export objects related to project if not embedded
        for i in LIST:
            for j in self._get_objects(i):
                _obj = constructor_from_dict(i)(j)
                if not _obj.embedded:
                    _obj.export()

    @staticmethod
    def _parse_spec(obj: dict) -> dict:
        """
        Parse spec dictionary.

        Parameters
        ----------
        obj : dict
            Project dictionary.

        Returns
        -------
        dict
            New project dictionary.
        """
        spec = obj.get("spec", {})
        new_spec: dict[str, list] = {}
        for i in spec:
            new_spec[i] = []
            for j in spec[i]:
                if not j.get("embedded", False):
                    _dict = {k: v for k, v in j.items() if k in ["kind", "name", "id"]}
                    new_spec[i].append(_dict)
                else:
                    new_spec[i].append(j)
        obj["spec"] = new_spec
        return obj

    #############################
    #  Generic operations for objects (artifacts, functions, workflows, dataitems)
    #############################

    def _add_object(self, obj: Entities, kind: str) -> None:
        """
        Add object to project as specification.

        Parameters
        ----------
        obj : Entity
            Object to be added to project.
        kind : str
            Kind of object to be added to project.

        Returns
        -------
        None
        """
        self._check_kind(kind)
        attr = getattr(self.spec, kind, []) + [obj.to_dict()]
        setattr(self.spec, kind, attr)

    def _delete_object(self, name: str, kind: str, uuid: str | None = None) -> None:
        """
        Delete object from project.

        Parameters
        ----------
        name : str
            Name of object to be deleted.
        kind : str
            Kind of object to be deleted.
        uuid : str
            UUID.

        Returns
        -------
        None
        """
        if uuid is None:
            attr_name = "name"
            var = name
        else:
            attr_name = "id"
            var = uuid
        self._check_kind(kind)
        spec_list = getattr(self.spec, kind, [])
        setattr(self.spec, kind, [i for i in spec_list if i.get(attr_name) != var])

    def _get_objects(self, kind: str) -> list[dict]:
        """
        Get dtos objects related to project.

        Parameters
        ----------
        kind : str
            Kind of object to be retrieved.

        Returns
        -------
        list[dict]
            List of objects related to project.

        Raises
        ------
        EntityError
            If kind is not valid.
        """
        self._check_kind(kind)
        return getattr(self.spec, kind, [])

    @staticmethod
    def _check_kind(kind: str) -> None:
        """
        Check if kind is valid.

        Parameters
        ----------
        kind : str
            Kind of object to be checked.

        Returns
        -------
        None

        Raises
        ------
        EntityError
            If kind is not valid.
        """
        if kind not in LIST:
            raise EntityError(f"Kind {kind} is not valid.")

    #############################
    #  Artifacts
    #############################

    def new_artifact(self, **kwargs) -> Artifact:
        """
        Create an instance of the Artifact class with the provided parameters.

        Parameters
        ----------
        **kwargs
            Keyword arguments.

        Returns
        -------
        Artifact
           Object instance.


        """
        kwargs["project"] = self.metadata.name
        obj = new_artifact(**kwargs)
        self._add_object(obj, ARTF)
        return obj

    def get_artifact(self, name: str, uuid: str | None = None) -> Artifact:
        """
        Get a Artifact from backend.

        Parameters
        ----------
        name : str
            Identifier of the artifact.
        uuid : str
            Identifier of the artifact version.

        Returns
        -------
        Artifact
            Instance of Artifact class.
        """
        obj = get_artifact(
            project=self.metadata.name,
            name=name,
            uuid=uuid,
        )
        self._add_object(obj, ARTF)
        return obj

    def delete_artifact(self, name: str, uuid: str | None = None) -> None:
        """
        Delete a Artifact from project.

        Parameters
        ----------
        name : str
            Identifier of the artifact.
        uuid : str
            Identifier of the artifact version.

        Returns
        -------
        None
        """
        if not self.local:
            delete_artifact(self.metadata.name, name)
        self._delete_object(name, ARTF, uuid=uuid)

    def set_artifact(self, artifact: Artifact) -> None:
        """
        Set a Artifact.

        Parameters
        ----------
        artifact : Artifact
            Artifact to set.

        Returns
        -------
        None
        """
        self._add_object(artifact, ARTF)

    #############################
    #  Functions
    #############################

    def new_function(self, **kwargs) -> Function:
        """
        Create a Function instance with the given parameters.

        Parameters
        ----------
        **kwargs
            Keyword arguments.

        Returns
        -------
        Function
           Object instance.


        """
        kwargs["project"] = self.metadata.name
        obj = new_function(**kwargs)
        self._add_object(obj, FUNC)
        return obj

    def get_function(self, name: str, uuid: str | None = None) -> Function:
        """
        Get a Function from backend.

        Parameters
        ----------
        name : str
            Identifier of the function.
        uuid : str
            Identifier of the function version.

        Returns
        -------
        Function
            Instance of Function class.
        """
        obj = get_function(
            project=self.metadata.name,
            name=name,
            uuid=uuid,
        )
        self._add_object(obj, FUNC)
        return obj

    def delete_function(self, name: str, uuid: str | None = None) -> None:
        """
        Delete a Function from project.

        Parameters
        ----------
        name : str
            Identifier of the function.
        uuid : str
            Identifier of the function version.

        Returns
        -------
        None
        """
        if not self.local:
            delete_function(self.metadata.name, name)
        self._delete_object(name, FUNC, uuid=uuid)

    def set_function(self, function: Function) -> None:
        """
        Set a Function.

        Parameters
        ----------
        function : Function
            Function to set.

        Returns
        -------
        None
        """
        self._add_object(function, FUNC)

    #############################
    #  Workflows
    #############################

    def new_workflow(self, **kwargs) -> Workflow:
        """
        Create a new Workflow instance with the specified parameters.

        Parameters
        ----------
        **kwargs
            Keyword arguments.

        Returns
        -------
        Workflow
            An instance of the created workflow.


        """
        kwargs["project"] = self.metadata.name
        obj = new_workflow(**kwargs)
        self._add_object(obj, WKFL)
        return obj

    def get_workflow(self, name: str, uuid: str | None = None) -> Workflow:
        """
        Get a Workflow from backend.

        Parameters
        ----------
        name : str
            Identifier of the workflow.
        uuid : str
            Identifier of the workflow version.

        Returns
        -------
        Workflow
            Instance of Workflow class.
        """
        obj = get_workflow(
            project=self.metadata.name,
            name=name,
            uuid=uuid,
        )
        self._add_object(obj, WKFL)
        return obj

    def delete_workflow(self, name: str, uuid: str | None = None) -> None:
        """
        Delete a Workflow from project.

        Parameters
        ----------
        name : str
            Identifier of the workflow.
        uuid : str
            Identifier of the workflow version.

        Returns
        -------
        None
        """
        if not self.local:
            delete_workflow(self.metadata.name, name)
        self._delete_object(name, WKFL, uuid=uuid)

    def set_workflow(self, workflow: Workflow) -> None:
        """
        Set a Workflow.

        Parameters
        ----------
        workflow : Workflow
            Workflow to set.

        Returns
        -------
        None
        """
        self._add_object(workflow, WKFL)

    #############################
    #  Dataitems
    #############################

    def new_dataitem(self, **kwargs) -> Dataitem:
        """
        Create a Dataitem.

        Parameters
        ----------
        **kwargs
            Keyword arguments.

        Returns
        -------
        Dataitem
           Object instance.


        """
        kwargs["project"] = self.metadata.name
        obj = new_dataitem(**kwargs)
        self._add_object(obj, DTIT)
        return obj

    def get_dataitem(self, name: str, uuid: str | None = None) -> Dataitem:
        """
        Get a Dataitem from backend.

        Parameters
        ----------
        name : str
            Identifier of the dataitem.
        uuid : str
            Identifier of the dataitem version.

        Returns
        -------
        Dataitem
            Instance of Dataitem class.
        """
        obj = get_dataitem(
            project=self.metadata.name,
            name=name,
            uuid=uuid,
        )
        self._add_object(obj, DTIT)
        return obj

    def delete_dataitem(self, name: str, uuid: str | None = None) -> None:
        """
        Delete a Dataitem from project.

        Parameters
        ----------
        name : str
            Identifier of the dataitem.
        uuid : str
            Identifier of the dataitem version.

        Returns
        -------
        None
        """
        if not self.local:
            delete_dataitem(self.metadata.name, name)
        self._delete_object(name, DTIT, uuid=uuid)

    def set_dataitem(self, dataitem: Dataitem) -> None:
        """
        Set a Dataitem.

        Parameters
        ----------
        dataitem : Dataitem
            Dataitem to set.

        Returns
        -------
        None
        """
        self._add_object(dataitem, DTIT)

    #############################
    #  Getters and Setters
    #############################

    @property
    def client(self) -> Client:
        """
        Get client.

        Returns
        -------
        Client
            Client instance.

        Raises
        ------
        EntityError
            If client is not specified.
        """
        if self._client is not None:
            return self._client
        raise EntityError("Client is not specified.")

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
    def from_dict(cls, obj: dict) -> "Project":
        """
        Create object instance from a dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create object from.

        Returns
        -------
        Project
            Self instance.
        """
        parsed_dict = cls._parse_dict(obj)
        _obj = cls(**parsed_dict)
        return _obj

    @staticmethod
    def _parse_dict(obj: dict) -> dict:
        """
        Parse a dictionary and return a parsed dictionary.

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
        name = obj.get("name")
        if name is None:
            raise EntityError("Name is not specified.")

        # Build UUID, kind, metadata, spec and status
        uuid = obj.get("id")
        uuid = build_uuid(uuid)

        kind = obj.get("kind")
        kind = build_kind(PROJ, kind)

        metadata = obj.get("metadata")
        metadata = (
            metadata
            if metadata is not None
            else {"project": name, "name": name, "version": uuid}
        )
        metadata = build_metadata(ARTF, **metadata)

        spec = obj.get("spec")
        spec = spec if spec is not None else {}
        spec = build_spec(PROJ, kind=kind, **spec)

        status = obj.get("status")
        status = status if status is not None else {}
        status = build_status(PROJ, **status)

        return {
            "uuid": uuid,
            "kind": kind,
            "metadata": metadata,
            "spec": spec,
            "status": status,
        }


def project_from_parameters(
    name: str,
    description: str | None = None,
    kind: str | None = None,
    context: str = "",
    source: str = "",
    local: bool = False,
    uuid: str | None = None,
    **kwargs,
) -> Project:
    """
    Create project.

    Parameters
    ----------
    name : str
        Identifier of the project.
    description : str
        Description of the project.
    kind : str
        The type of the project.
    context : str
        The context of the project.
    source : str
        The source of the project.
    local : bool
        Flag to determine if object will be exported to backend.
    uuid : str
        UUID.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Project
        Project object.
    """
    uuid = build_uuid(uuid)
    kind = build_kind(PROJ, kind)
    spec = build_spec(
        PROJ,
        kind,
        context=context,
        source=source,
        **kwargs,
    )
    metadata = build_metadata(
        PROJ,
        project=name,
        name=name,
        version=uuid,
        description=description,
    )
    status = build_status(PROJ)
    return Project(
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
        local=local,
    )


def project_from_dict(obj: dict) -> Project:
    """
    Create project from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create project from.

    Returns
    -------
    Project
        Project object.
    """
    return Project.from_dict(obj)
