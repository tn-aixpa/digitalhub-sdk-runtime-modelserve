"""
Project module.
"""
from __future__ import annotations

import typing
from dataclasses import dataclass, field

from sdk.client.factory import get_client
from sdk.entities.api import (
    create_api_proj,
    update_api_project,
    DTO_ARTF,
    DTO_DTIT,
    DTO_FUNC,
    DTO_WKFL,
)
from sdk.entities.artifact.artifact import Artifact
from sdk.entities.artifact.operations import delete_artifact, new_artifact
from sdk.entities.dataitem.dataitem import Dataitem
from sdk.entities.dataitem.operations import delete_dataitem, new_dataitem
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.entities.function.function import Function
from sdk.entities.function.operations import delete_function, new_function
from sdk.entities.workflow.operations import delete_workflow, new_workflow
from sdk.entities.workflow.workflow import Workflow
from sdk.utils.utils import get_uiid

if typing.TYPE_CHECKING:
    from sdk.client.client import Client


@dataclass
class ProjectMetadata(EntityMetadata):
    ...


@dataclass
class ProjectSpec(EntitySpec):
    context: str = "./"
    source: str = None
    functions: list = field(default_factory=list)
    artifacts: list = field(default_factory=list)
    workflows: list = field(default_factory=list)
    dataitems: list = field(default_factory=list)


class Project(Entity):
    """
    A class representing a project.
    """

    def __init__(
        self,
        name: str,
        metadata: ProjectMetadata = None,
        spec: ProjectSpec = None,
        local: bool = False,
        **kwargs,
    ) -> None:
        """
        Initialize the Project instance.

        Parameters
        ----------
        name : str
            Name of the project.
        metadata : ProjectMetadata, optional
            Metadata for the function, default is None.
        spec : ProjectSpec, optional
            Specification for the function, default is None.
        local: bool, optional
            Specify if run locally, default is False.
        **kwargs
            Additional keyword arguments.
        """
        super().__init__()
        self.name = name
        self.kind = "project"
        self.metadata = metadata if metadata is not None else ProjectMetadata(name=name)
        self.spec = spec if spec is not None else ProjectSpec()
        self._local = local
        self._client = get_client()

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        # Set id if None
        if self.id is None:
            self.id = get_uiid()

    def save(self, save_object: bool = False, overwrite: bool = False) -> dict:
        """
        Save project and context into backend.

        Parameters
        ----------
        save_object : bool, optional
            Flag to determine if object related to project will be saved.
        overwrite : bool, optional
            Flag to determine if object will be overwritten.

        Returns
        -------
        dict
            Mapping representation of Project from backend.

        """
        responses = []
        if self._local:
            raise Exception("Use .export() for local execution.")

        obj = self._parse_obj(self.to_dict())

        if overwrite:
            api = update_api_project(self.name)
            r = self.client.update_object(obj, api)
        else:
            api = create_api_proj()
            r = self.client.create_object(obj, api)

        responses.append(r)

        if save_object:
            for i in [DTO_ARTF, DTO_FUNC, DTO_WKFL]:
                for o in self._get_spec_objects(i):
                    r = o.save()
                    responses.append(r)

        return responses

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
        spec = obj.get("spec", {})
        l = [DTO_ARTF, DTO_FUNC, DTO_WKFL]
        for i in l:
            tmp = []
            for o in spec.get(i, []):
                if o._embed:
                    tmp.append(o.to_dict())
                else:
                    o.export()
                    tmp.append(o.to_dict_not_embed())
            spec[i] = tmp
        obj["spec"] = spec
        filename = filename if filename is not None else f"project.yaml"
        return self.export_object(filename, obj)

    @classmethod
    def from_dict(cls, d: dict) -> "Project":
        """
        Create Project instance from a dictionary.

        Parameters
        ----------
        d : dict
            Dictionary to create Project from.

        Returns
        -------
        Project
            Project instance.

        """
        name = d.get("name")
        if name is None:
            raise Exception("Project or name is not specified.")
        metadata = ProjectMetadata.from_dict(d.get("metadata", {"name": name}))
        spec = ProjectSpec.from_dict(d.get("spec", {}))
        spec.functions = [Function.from_dict(i) for i in spec.functions]
        spec.artifacts = [Artifact.from_dict(i) for i in spec.artifacts]
        spec.workflows = [Workflow.from_dict(i) for i in spec.workflows]
        spec.dataitems = [Dataitem.from_dict(i) for i in spec.dataitems]
        return cls(name, metadata=metadata, spec=spec)

    #############################
    #  CRUD operations
    #############################

    @property
    def client(self) -> Client:
        """
        Get client.
        """
        return self._client

    @property
    def local(self) -> bool:
        """
        Get local flag.
        """
        return self._local

    def _parse_obj(self, obj: dict) -> None:
        l = [DTO_ARTF, DTO_FUNC, DTO_WKFL]
        for i in l:
            obj[i] = []
        obj["spec"] = {k: v for k, v in obj.get("spec", {}).items() if k not in l}
        return obj

    def _set_spec_object(self, obj: Entity, kind: str) -> None:
        setattr(self.spec, kind, getattr(self.spec, kind, []) + [obj])

    def _get_spec_object(self, name: str, kind: str) -> Entity:
        obj_list = self._get_spec_objects(kind)
        return next((i for i in obj_list if i.name == name), None)

    def _get_spec_objects(self, kind: str) -> list:
        return getattr(self.spec, kind, [])

    def _remove_spec_object(self, name: str, kind: str) -> None:
        setattr(
            self.spec, kind, [i for i in getattr(self.spec, kind) if i.name != name]
        )
        if not self._local:
            delete_function(self._client, name)

    #############################
    #  Artifacts
    #############################

    def new_artifact(
        self,
        name: str,
        description: str = None,
        kind: str = None,
        key: str = None,
        source: str = None,
        target_path: str = None,
        local: bool = False,
        embed: bool = False,
    ) -> Artifact:
        """
        Create an instance of the Artifact class with the provided parameters.

        Parameters
        ----------
        name : str
            Identifier of the artifact.
        description : str, optional
            Description of the artifact.
        kind : str, optional
            The type of the artifact.
        key : str
            Representation of artfact like store://etc..
        source : str
            Path to the artifact on local file system or remote storage.
        target_path : str
            Path of destionation for the artifact.
        local : bool, optional
            Flag to determine if object has local execution.
        embed : bool, optional
            Flag to determine if object must be embedded in project.

        Returns
        -------
        Artifact
            Instance of the Artifact class representing the specified artifact.
        """
        return new_artifact(
            project=self.name,
            name=name,
            description=description,
            kind=kind,
            key=key,
            source=source,
            target_path=target_path,
            local=local,
            embed=embed,
        )

    def add_artifact(self, artifact: Artifact) -> dict:
        r = self._set_spec_object(artifact, DTO_ARTF)
        return r

    def remove_artifact(self, name: str) -> None:
        self._remove_spec_object(name, DTO_ARTF)
        if not self._local:
            delete_artifact(self._client, name)

    def get_artifact(self, name: str) -> Artifact:
        return self._get_spec_object(name, DTO_ARTF)

    def get_artifacts(self) -> list:
        return self._get_spec_objects(DTO_ARTF)

    #############################
    #  Functions
    #############################

    def new_function(
        self,
        name: str,
        description: str = None,
        kind: str = None,
        source: str = None,
        image: str = None,
        tag: str = None,
        handler: str = None,
        local: bool = False,
        embed: bool = False,
    ) -> Function:
        """
        Create a Function instance with the given parameters.

        Parameters
        ----------
        project : str
            Name of the project.
        name : str
            Identifier of the Function.
        description : str, optional
            Description of the Function.
        kind : str, optional
            The type of the Function.
        source : str, optional
            Path to the Function's source code on the local file system or remote storage.
        image : str, optional
            Name of the Function's Docker image.
        tag : str, optional
            Tag of the Function's Docker image.
        handler : str, optional
            Function handler name.
        local : bool, optional
            Flag to determine if object has local execution.
        embed : bool, optional
            Flag to determine if object must be embedded in project.

        Returns
        -------
        Function
            Instance of the Function class representing the specified function.
        """
        return new_function(
            project=self.name,
            name=name,
            description=description,
            kind=kind,
            source=source,
            image=image,
            tag=tag,
            handler=handler,
            local=local,
            embed=embed,
        )

    def add_function(self, function: Function) -> dict:
        r = self._set_spec_object(function, DTO_FUNC)
        return r

    def remove_function(self, name: str) -> None:
        self._remove_spec_object(name, DTO_FUNC)
        if not self._local:
            delete_function(self._client, name)

    def get_function(self, name: str) -> Function:
        return self._get_spec_object(name, DTO_FUNC)

    def get_functions(self) -> list:
        return self._get_spec_objects(DTO_FUNC)

    #############################
    #  Workflows
    #############################

    def new_workflow(
        self,
        name: str,
        description: str = None,
        kind: str = None,
        test: str = None,
        local: bool = False,
        embed: bool = False,
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
        embed : bool, optional
            Flag to determine if object must be embedded in project.

        Returns
        -------
        Workflow
            An instance of the created workflow.
        """
        return new_workflow(
            project=self.name,
            name=name,
            description=description,
            kind=kind,
            test=test,
            local=local,
            embed=embed,
        )

    def add_workflow(self, workflow: Workflow) -> dict:
        r = self._set_spec_object(workflow, DTO_WKFL)
        return r

    def remove_workflow(self, name: str) -> None:
        self._remove_spec_object(name, DTO_WKFL)
        if not self._local:
            delete_workflow(self._client, name)

    def get_workflow(self, name: str) -> Workflow:
        return self._get_spec_object(name, DTO_WKFL)

    def get_workflows(self) -> list:
        return self._get_spec_objects(DTO_WKFL)

    #############################
    #  Dataitems
    #############################

    def new_dataitem(
        self,
        name: str,
        description: str = None,
        kind: str = None,
        key: str = None,
        path: str = None,
        local: bool = False,
        embed: bool = False,
    ) -> Dataitem:
        """
        Create an Dataitem instance with the given parameters.

        Parameters
        ----------
        name : str
            Identifier of the dataitem.
        description : str, optional
            Description of the dataitem.
        kind : str, optional
            The type of the dataitem.
        key : str
            Representation of artfact like store://etc..
        path : str
            Path to the dataitem on local file system or remote storage.
        local : bool, optional
            Flag to determine if object has local execution.
        embed : bool, optional
            Flag to determine if object must be embedded in project.

        Returns
        -------
        Dataitem
            Instance of the Dataitem class representing the specified dataitem.
        """
        return new_dataitem(
            project=self.name,
            name=name,
            description=description,
            kind=kind,
            key=key,
            path=path,
            local=local,
            embed=embed,
        )

    def add_dataitem(self, dataitem: Dataitem) -> dict:
        r = self._set_spec_object(dataitem, DTO_DTIT)
        return r

    def remove_dataitem(self, name: str) -> None:
        self._remove_spec_object(name, DTO_DTIT)
        if not self._local:
            delete_dataitem(self._client, name)

    def get_dataitem(self, name: str) -> Dataitem:
        return self._get_spec_object(name, DTO_DTIT)

    def get_dataitems(self) -> list:
        return self._get_spec_objects(DTO_DTIT)
