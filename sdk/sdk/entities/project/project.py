"""
Project module.
"""
from sdk.client.client import Client
from sdk.entities.base_entity import Entity
from sdk.entities.artifact.artifact import Artifact
from sdk.entities.artifact.operations import delete_artifact
from sdk.entities.function.function import Function
from sdk.entities.function.operations import delete_function
from sdk.entities.workflow.workflow import Workflow
from sdk.entities.workflow.operations import delete_workflow


class Project(Entity):
    """
    A class representing a project.

    Parameters
    ----------
    name : str
        The name of the project.
    source : str, optional
        The source of the project (eg. git://repo-url).
    description : str, optional
        The description of the project.

    Methods
    -------
    new()
        Create a new project and an execution context.

    load()
        Load project and context from backend.

    save()
        Save project and context into backend.

    to_dict()
        Return object to dict.

    __repr__()
        Return string representation of the project object.

    Attributes
    ----------
    name : str
        The name of the project.
    source : str or None
        The source of the project (eg. git://repo-url).
    description : str or None
        The description of the project.

    """

    API_CREATE = "/api/v1/projects"

    def __init__(
        self,
        name: str,
        source: str = "",
        description: str = "",
        functions: list = None,
        artifacts: list = None,
        workflows: list = None,
    ) -> None:
        """Initialize the Project instance."""
        self.name = name
        self.source = source
        self.description = description
        self.functions = functions if functions is not None else []
        self.artifacts = artifacts if artifacts is not None else []
        self.workflows = workflows if workflows is not None else []
        self.id = None

    def save(self, client: Client, overwrite: bool = False) -> dict:
        """
        Save project and context into backend.

        Returns
        -------
        dict
            Mapping representaion of Project from backend.

        """
        try:
            r = client.create_object(self.to_dict(), self.API_CREATE)
            self.id = r["id"]
            return r
        except KeyError:
            raise Exception("Project already present in the backend.")

    def set_artifact(self, client: Client, artifact: Artifact) -> dict:
        r = artifact.save(client)
        if "status" not in r:
            self.artifacts.append(artifact.to_dict())
            return r
        raise Exception(f"Backend error: {r['status']}")

    def unset_artifact(self, client: Client, key: str) -> None:
        delete_artifact(client, key)
        self.artifacts = [i for i in self.artifacts if i["key"] != key]

    def set_function(self, client: Client, function: Function) -> dict:
        r = function.save(client)
        if "status" not in r:
            self.functions.append(function.to_dict())
            return r
        raise Exception(f"Backend error: {r['status']}")

    def unset_function(self, client: Client, key: str) -> None:
        delete_function(client, key)
        self.functions = [i for i in self.functions if i["name"] != key]

    def set_workflow(self, client: Client, workflow: Workflow) -> dict:
        r = workflow.save(client)
        if "status" not in r:
            self.workflows.append(workflow.to_dict())
            return r
        raise Exception(f"Backend error: {r['status']}")

    def unset_workflow(self, client: Client, key: str) -> None:
        delete_workflow(client, key)
        self.workflows = [i for i in self.workflows if i["name"] != key]
