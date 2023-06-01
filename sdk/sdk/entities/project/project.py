"""
Project module.
"""
from sdk.client.client import Client
from sdk.entities.artifact.artifact import Artifact
from sdk.entities.artifact.operations import delete_artifact
from sdk.entities.base_entity import Entity, EntityMetadata, EntitySpec
from sdk.entities.function.function import Function
from sdk.entities.function.operations import delete_function
from sdk.entities.workflow.operations import delete_workflow
from sdk.entities.workflow.workflow import Workflow
from sdk.utils.common import API_CREATE, DTO_PROJ
from sdk.utils.utils import get_uiid


class ProjectMetadata(EntityMetadata):
    name: str = None
    description: str = None


class ProjectSpec(EntitySpec):
    context: str = "./"
    source: str = None
    functions: list = None
    artifacts: list = None
    workflows: list = None


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
        self.metadata = metadata if metadata is not None else {}
        self.spec = spec if spec is not None else {}
        self._local = local

        # Set new attributes
        for k, v in kwargs.items():
            if k not in self._obj_attr:
                self.__setattr__(k, v)

        # Set id if None
        if self.id is None:
            self.id = get_uiid()

    def save(self, client: Client = None, overwrite: bool = False) -> dict:
        """
        Save project and context into backend.

        Returns
        -------
        dict
            Mapping representaion of Project from backend.

        """
        if self._local:
            self.export()
        api = API_CREATE.format(self.name, DTO_PROJ)
        return self.save_object(client, self.to_dict(), api, overwrite)

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

    def set_artifact(self, client: Client, artifact: Artifact) -> dict:
        r = artifact.save(client)
        if "status" not in r:
            self.artifacts.append(artifact)
            return r
        raise Exception(f"Backend error: {r['status']}")

    def unset_artifact(self, client: Client, key: str) -> None:
        delete_artifact(client, key)
        self.artifacts = [i for i in self.artifacts if i["key"] != key]

    def set_function(self, client: Client, function: Function) -> dict:
        r = function.save(client)
        if "status" not in r:
            self.functions.append(function)
            return r
        raise Exception(f"Backend error: {r['status']}")

    def unset_function(self, client: Client, key: str) -> None:
        delete_function(client, key)
        self.functions = [i for i in self.functions if i["name"] != key]

    def set_workflow(self, client: Client, workflow: Workflow) -> dict:
        r = workflow.save(client)
        if "status" not in r:
            self.workflows.append(workflow)
            return r
        raise Exception(f"Backend error: {r['status']}")

    def unset_workflow(self, client: Client, key: str) -> None:
        delete_workflow(client, key)
        self.workflows = [i for i in self.workflows if i["name"] != key]
