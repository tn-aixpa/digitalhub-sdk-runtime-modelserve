"""
Project module.
"""
from __future__ import annotations

import typing
from typing import TypeVar, Callable

from sdk.entities.artifact.crud import (
    create_artifact_from_dict,
    delete_artifact,
    get_artifact,
    new_artifact,
)
from sdk.entities.base.entity import Entity
from sdk.entities.dataitem.crud import (
    create_dataitem_from_dict,
    delete_dataitem,
    get_dataitem,
    new_dataitem,
)
from sdk.entities.function.crud import (
    create_function_from_dict,
    delete_function,
    get_function,
    new_function,
)
from sdk.entities.project.metadata import build_metadata
from sdk.entities.project.spec.builder import build_spec
from sdk.entities.utils.utils import get_uiid
from sdk.entities.workflow.crud import (
    create_workflow_from_dict,
    delete_workflow,
    get_workflow,
    new_workflow,
)
from sdk.utils.api import (
    DTO_ARTF,
    DTO_DTIT,
    DTO_FUNC,
    DTO_PROJ,
    DTO_WKFL,
    api_base_create,
)
from sdk.utils.exceptions import BackendError, EntityError
from sdk.utils.factories import get_client, set_context

if typing.TYPE_CHECKING:
    from sdk.client.client import Client
    from sdk.entities.artifact.entity import Artifact
    from sdk.entities.dataitem.entity import Dataitem
    from sdk.entities.function.entity import Function
    from sdk.entities.project.metadata import ProjectMetadata
    from sdk.entities.project.spec.builder import ProjectSpec
    from sdk.entities.workflow.entity import Workflow

    Entities = TypeVar("Entities", Artifact, Function, Workflow, Dataitem)


DTO_LIST = [DTO_ARTF, DTO_FUNC, DTO_WKFL, DTO_DTIT]
SPEC_LIST = DTO_LIST + ["source", "context"]


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
    if dto == DTO_ARTF:
        return create_artifact_from_dict
    if dto == DTO_FUNC:
        return create_function_from_dict
    if dto == DTO_WKFL:
        return create_workflow_from_dict
    if dto == DTO_DTIT:
        return create_dataitem_from_dict
    raise EntityError(f"DTO {dto} is not valid.")


class Project(Entity):
    """
    A class representing a project.
    """

    def __init__(
        self,
        name: str,
        metadata: ProjectMetadata | None = None,
        spec: ProjectSpec | None = None,
        local: bool = False,
        uuid: str | None = None,
        **kwargs,
    ) -> None:
        """
        Initialize the Project instance.

        Parameters
        ----------
        name : str
            Name of the object.
        metadata : ProjectMetadata
            Metadata of the object.
        spec : ProjectSpec
            Specification of the object.
        local: bool
            If True, run locally.
        **kwargs
            Keyword arguments.
        """
        super().__init__()
        self.name = name
        self.kind = "project"
        self.id = get_uiid(uuid=uuid)
        self.metadata = metadata if metadata is not None else build_metadata(name=name)
        self.spec = spec if spec is not None else build_spec(self.kind, **{})

        # Set new attributes
        self._any_setter(**kwargs)

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

        # Try to create project
        # (try to avoid error response if project already exists)
        try:
            api = api_base_create(DTO_PROJ)
            response = self.client.create_object(obj, api)
            responses[DTO_PROJ] = response
        except BackendError:
            responses[DTO_PROJ] = obj

        # Try to save objects related to project
        # (try to avoid error response if object does not exists)
        for i in DTO_LIST:
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
        for i in DTO_LIST:
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
        if kind not in DTO_LIST:
            raise EntityError(f"Kind {kind} is not valid.")

    #############################
    #  Artifacts
    #############################

    def new_artifact(
        self,
        name: str,
        description: str = "",
        kind: str = "artifact",
        key: str | None = None,
        src_path: str | None = None,
        target_path: str | None = None,
        local: bool = False,
        embedded: bool = False,
        uuid: str | None = None,
    ) -> Artifact:
        """
        Create an instance of the Artifact class with the provided parameters.

        Parameters
        ----------
        name : str
            Identifier of the artifact.
        description : str
            Description of the artifact.
        kind : str
            The type of the artifact.
        key : str
            Representation of artfact like store://etc..
        src_path : str
            Path to the artifact on local file system.
        target_path : str
            Path of destionation for the artifact.
        local : bool
            Flag to determine if object has local execution.
        embedded : bool
            Flag to determine if object must be embedded in project.
        uuid : str
            UUID.

        Returns
        -------
        Artifact
           Object instance.
        """
        obj = new_artifact(
            project=self.name,
            name=name,
            description=description,
            kind=kind,
            key=key,
            src_path=src_path,
            target_path=target_path,
            local=local,
            embedded=embedded,
            uuid=uuid,
        )
        self._add_object(obj, DTO_ARTF)
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
            project=self.name,
            name=name,
            uuid=uuid,
        )
        self._add_object(obj, DTO_ARTF)
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
            delete_artifact(self.name, name)
        self._delete_object(name, DTO_ARTF, uuid=uuid)

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
        self._add_object(artifact, DTO_ARTF)

    #############################
    #  Functions
    #############################

    def new_function(
        self,
        name: str,
        description: str = "",
        kind: str = "job",
        source: str | None = None,
        image: str | None = None,
        tag: str | None = None,
        handler: str | None = None,
        command: str | None = None,
        requirements: list | None = None,
        sql: str | None = None,
        local: bool = False,
        embedded: bool = False,
        uuid: str | None = None,
    ) -> Function:
        """
        Create a Function instance with the given parameters.

        Parameters
        ----------
        name : str
            Identifier of the Function.
        description : str
            Description of the Function.
        kind : str, default "job"
            The type of the Function.
        source : str
            Path to the Function's source code on the local file system.
        image : str
            Name of the Function's container image.
        tag : str
            Tag of the Function's container image.
        handler : str
            Function handler name.
        command : str
            Command to run inside the container.
        requirements : list
            List of requirements for the Function.
        sql : str
            SQL query.
        local : bool
            Flag to determine if object has local execution.
        embedded : bool
            Flag to determine if object must be embedded in project.
        uuid : str
            UUID.

        Returns
        -------
        Function
           Object instance.
        """
        obj = new_function(
            project=self.name,
            name=name,
            description=description,
            kind=kind,
            source=source,
            image=image,
            tag=tag,
            handler=handler,
            command=command,
            requirements=requirements,
            sql=sql,
            local=local,
            embedded=embedded,
            uuid=uuid,
        )
        self._add_object(obj, DTO_FUNC)
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
            project=self.name,
            name=name,
            uuid=uuid,
        )
        self._add_object(obj, DTO_FUNC)
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
            delete_function(self.name, name)
        self._delete_object(name, DTO_FUNC, uuid=uuid)

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
        self._add_object(function, DTO_FUNC)

    #############################
    #  Workflows
    #############################

    def new_workflow(
        self,
        name: str,
        description: str = "",
        kind: str = "job",
        test: str | None = None,
        local: bool = False,
        embedded: bool = False,
        uuid: str | None = None,
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
        spec_ : dict
            Specification of the object.
        local : bool
            Flag to determine if object has local execution.
        embedded : bool
            Flag to determine if object must be embedded in project.
        uuid : str
            UUID.

        Returns
        -------
        Workflow
            An instance of the created workflow.
        """
        obj = new_workflow(
            project=self.name,
            name=name,
            description=description,
            kind=kind,
            test=test,
            local=local,
            embedded=embedded,
            uuid=uuid,
        )
        self._add_object(obj, DTO_WKFL)
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
            project=self.name,
            name=name,
            uuid=uuid,
        )
        self._add_object(obj, DTO_WKFL)
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
            delete_workflow(self.name, name)
        self._delete_object(name, DTO_WKFL, uuid=uuid)

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
        self._add_object(workflow, DTO_WKFL)

    #############################
    #  Dataitems
    #############################

    def new_dataitem(
        self,
        name: str,
        description: str = "",
        kind: str = "dataitem",
        key: str | None = None,
        path: str | None = None,
        local: bool = False,
        embedded: bool = False,
        uuid: str | None = None,
    ) -> Dataitem:
        """
        Create a Dataitem.

        Parameters
        ----------
        name : str
            Identifier of the dataitem.
        description : str
            Description of the dataitem.
        kind : str
            The type of the dataitem.
        key : str
            Representation of artfact like store://etc..
        path : str
            Path to the dataitem on local file system or remote storage.
        local : bool
            Flag to determine if object has local execution.
        embedded : bool
            Flag to determine if object must be embedded in project.
        uuid : str
            UUID.

        Returns
        -------
        Dataitem
           Object instance.
        """
        obj = new_dataitem(
            project=self.name,
            name=name,
            description=description,
            kind=kind,
            key=key,
            path=path,
            local=local,
            embedded=embedded,
            uuid=uuid,
        )
        self._add_object(obj, DTO_DTIT)
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
            project=self.name,
            name=name,
            uuid=uuid,
        )
        self._add_object(obj, DTO_DTIT)
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
            delete_dataitem(self.name, name)
        self._delete_object(name, DTO_DTIT, uuid=uuid)

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
        self._add_object(dataitem, DTO_DTIT)

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

        # Optional fields
        uuid = obj.get("id")
        kind = obj.get("kind", "project")

        # Build metadata and spec
        _spec = {k: v for k, v in obj.get("spec", {}).items() if k in SPEC_LIST}
        spec = build_spec(kind=kind, **_spec)
        metadata = build_metadata(**obj.get("metadata", {"name": name}))

        return {
            "name": name,
            "kind": kind,
            "uuid": uuid,
            "metadata": metadata,
            "spec": spec,
        }


def project_from_parameters(
    name: str,
    description: str = "",
    kind: str = "project",
    context: str = "",
    source: str = "",
    local: bool = False,
    uuid: str | None = None,
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
        Flag to determine if object has local execution.
    uuid : str
        UUID.

    Returns
    -------
    Project
        Project object.
    """
    meta = build_metadata(name=name, description=description)
    spec = build_spec(kind, context=context, source=source)
    return Project(
        name=name,
        kind=kind,
        metadata=meta,
        spec=spec,
        local=local,
        uuid=uuid,
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
