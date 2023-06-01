"""
Project module.
"""
from sdk.entities.artifact.artifact import Artifact
from sdk.entities.artifact.operations import delete_artifact
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.entities.function.function import Function
from sdk.entities.function.operations import delete_function
from sdk.entities.workflow.operations import delete_workflow
from sdk.entities.workflow.workflow import Workflow
from sdk.utils.api import API_CREATE_PROJECT
from sdk.utils.utils import get_uiid
from dataclasses import dataclass, field


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
        self.metadata = metadata if metadata is not None else {}
        self.spec = spec if spec is not None else {}
        self._local = local
        self._embed = embed

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        # Set id if None
        if self.id is None:
            self.id = "test"  # get_uiid()

    def save(self, overwrite: bool = False) -> dict:
        """
        Save project and context into backend.

        Returns
        -------
        dict
            Mapping representaion of Project from backend.

        """
        if self._local:
            return self.export()
        api = API_CREATE_PROJECT
        obj = self.to_dict()
        obj["functions"] = obj.get("spec", {}).get("functions", [])
        obj["artifacts"] = obj.get("spec", {}).get("artifacts", [])
        obj["workflows"] = obj.get("spec", {}).get("workflows", [])
        l = ["functions", "artifacts", "workflows"]
        if "spec" in obj:
            obj["spec"] = {k: v for k, v in obj["spec"].items() if k not in l}
        return self.save_object(obj, api, overwrite)

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
        filename = filename if filename is not None else f"project.yaml"
        return self.export_object(filename, obj)

    def set_artifact(self, artifact: Artifact) -> dict:
        if not self._embed:
            obj = artifact.to_dict_not_embed()
        else:
            obj = artifact.to_dict()
        self.spec.artifacts.append(obj)
        if self._local:
            return
        r = artifact.save()
        if "status" not in r:
            return r
        raise Exception(f"Backend error: {r['status']}")

    def unset_artifact(self, name: str) -> None:
        self.artifacts = [i for i in self.artifacts if i["name"] != name]
        if not self._local:
            delete_artifact(self._client, name)

    def set_function(self, function: Function) -> dict:
        if not self._embed:
            obj = function.to_dict_not_embed()
        else:
            obj = function.to_dict()
        self.spec.functions.append(obj)
        if self._local:
            return
        r = function.save()
        if "status" not in r:
            return r
        raise Exception(f"Backend error: {r['status']}")

    def unset_function(self, name: str) -> None:
        self.functions = [i for i in self.functions if i["name"] != name]
        if not self._local:
            delete_function(self._client, name)

    def set_workflow(self, workflow: Workflow) -> dict:
        if not self._embed:
            obj = workflow.to_dict_not_embed()
        else:
            obj = workflow.to_dict()
        self.spec.workflows.append(obj)
        if self._local:
            return
        r = workflow.save()
        if "status" not in r:
            return r
        raise Exception(f"Backend error: {r['status']}")

    def unset_workflow(self, name: str) -> None:
        self.workflows = [i for i in self.workflows if i["name"] != name]
        if not self._local:
            delete_workflow(self._client, name)
