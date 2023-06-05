"""
Project module.
"""
from dataclasses import dataclass, field

from sdk.entities.artifact.artifact import Artifact
from sdk.entities.artifact.operations import delete_artifact
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.entities.function.function import Function
from sdk.entities.function.operations import delete_function

from sdk.entities.workflow.operations import delete_workflow
from sdk.entities.workflow.workflow import Workflow
from sdk.entities.api import API_CREATE_PROJECT, API_UPDATE_PROJECT, DTO_ARTF, DTO_DTIT, DTO_FUNC, DTO_WKFL
from sdk.utils.utils import get_uiid


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
        embed: bool = False,
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
        self._embed = embed

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
            Mapping representaion of Project from backend.

        """
        if self._local:
            raise Exception("Use .export() for local execution.")

        if overwrite:
            api = API_UPDATE_PROJECT.format(self.name)
        else:
            api = API_CREATE_PROJECT

        responses = []
        obj = self._parse_obj(self.to_dict())
        r = self.save_object(obj, api, overwrite)
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
                if self._embed:
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
        return cls(name, metadata=metadata, spec=spec)

    def _parse_obj(self, obj: dict) -> None:
        l = [DTO_ARTF, DTO_FUNC, DTO_WKFL]
        for i in l:
            obj[i] = []
        obj["spec"] = {k: v for k, v in obj.get("spec", {}).items() if k not in l}
        return obj

    def _set_spec_objects(self, obj: Entity, kind: str, save: bool, **kwargs) -> None:
        setattr(self.spec, kind, getattr(self.spec, kind, []) + [obj])
        if save:
            if self._local:
                obj.export(**kwargs)
            else:
                obj.save(**kwargs)

    def _get_spec_objects(self, kind: str) -> list:
        return getattr(self.spec, kind, [])

    def _get_spec_object(self, name: str, kind: str) -> Entity:
        obj_list = self._get_spec_objects(kind)
        return next((i for i in obj_list if i.name == name), None)

    def _remove_spec_object(self, name: str, kind: str) -> None:
        setattr(
            self.spec, kind, [i for i in getattr(self.spec, kind) if i.name != name]
        )
        if not self._local:
            delete_function(self._client, name)

    def set_artifact(self, artifact: Artifact, save: bool = False, **kwargs) -> dict:
        r = self._set_spec_objects(artifact, "artifacts", save, **kwargs)
        return r

    def remove_artifact(self, name: str) -> None:
        self._remove_spec_object(name, "artifacts")
        if not self._local:
            delete_artifact(self._client, name)

    def get_artifact(self, name: str) -> Artifact:
        return self._get_spec_object(name, "artifacts")

    def get_artifacts(self) -> list:
        return self._get_spec_objects("artifacts")

    def set_function(self, function: Function, save: bool = False, **kwargs) -> dict:
        r = self._set_spec_objects(function, "functions", save, **kwargs)
        return r

    def remove_function(self, name: str) -> None:
        self._remove_spec_object(name, "functions")
        if not self._local:
            delete_function(self._client, name)

    def get_function(self, name: str) -> Function:
        return self._get_spec_object(name, "functions")

    def get_functions(self) -> list:
        return self._get_spec_objects("functions")

    def set_workflow(self, workflow: Workflow, save: bool = False, **kwargs) -> dict:
        r = self._set_spec_objects(workflow, "workflows", save, **kwargs)
        return r

    def remove_workflow(self, name: str) -> None:
        self._remove_spec_object(name, "workflows")
        if not self._local:
            delete_workflow(self._client, name)

    def get_workflow(self, name: str) -> Workflow:
        return self._get_spec_object(name, "workflows")

    def get_workflows(self) -> list:
        return self._get_spec_objects("workflows")
