"""
Project module.
"""
from copy import deepcopy

from sdk.client.client import Client
from sdk.entities.utils import file_importer, file_exporter, delete_from_backend
from sdk.entities.artifact import Artifact, delete_artifact
from sdk.entities.function import Function, delete_function
from sdk.entities.workflow import Workflow, delete_workflow


API_CREATE = "/api/v1/projects"
API_READ = "/api/v1/projects/{}"
API_DELETE = "/api/v1/projects/{}"
API_READ_ALL = "/api/v1/projects"


OBJ_ATTR = [
    "name",
    "source",
    "description",
    "functions",
    "artifacts",
    "workflows",
]


class Project:
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
            r = client.create_object(self.to_dict(), API_CREATE)
            self.id = r["id"]
            return r
        except KeyError:
            raise Exception("Project already present in the backend.")

    def set_artifact(self, client: Client, artifact: Artifact) -> dict:
        r = artifact.save(client)
        if "status" not in r:
            self.artifacts.append(artifact)
            return r
        raise Exception(f"Backend error: {r['status']}")

    def unset_artifact(self, client: Client, key: str) -> None:
        delete_artifact(client, key)
        self.artifacts = [i for i in self.artifacts if i.key != key]

    def set_function(self, client: Client, function: Function) -> dict:
        r = function.save(client)
        if "status" not in r:
            self.functions.append(function)
            return r
        raise Exception(f"Backend error: {r['status']}")

    def unset_function(self, client: Client, key: str) -> None:
        delete_function(client, key)
        self.functions = [i for i in self.functions if i.name != key]

    def set_workflow(self, client: Client, workflow: Workflow) -> dict:
        r = workflow.save(client)
        if "status" not in r:
            self.workflows.append(workflow)
            return r
        raise Exception(f"Backend error: {r['status']}")

    def unset_workflow(self, client: Client, key: str) -> None:
        delete_workflow(client, key)
        self.workflows = [i for i in self.workflows if i.name != key]

    def to_dict(self) -> dict:
        """
        Return object to dict.

        Returns
        -------
        dict
            A dictionary containing the attributes of the Project instance.

        """
        dict_ = deepcopy(self.__dict__)
        dict_["functions"] = [i.to_dict() for i in dict_["functions"]]
        dict_["artifacts"] = [i.to_dict() for i in dict_["artifacts"]]
        dict_["workflows"] = [i.to_dict() for i in dict_["workflows"]]
        return {k: v for k, v in dict_.items() if v is not None}

    def __repr__(self) -> str:
        """
        Return string representation of the project object.

        Returns
        -------
        str
            A string representing the Project instance.

        """
        return str(self.to_dict())


def new_project(
    client: Client,
    name: str,
    source: str = None,
    description: str = None,
) -> Project:
    """
    Create a new project and an execution context.

    Parameters
    ----------
    client : Client
        A Client object to interact with backend.
    name : str
        The name of the project to load.
    source : str, optional
        The source of the project (eg. git://repo-url).
    description : str, optional
        The description of the project.

    Returns
    -------
    Project
        A Project instance with its context.

    """
    obj = Project(name, source, description)
    obj.save(client)
    return obj


def load_project(client: Client, name: str) -> Project:
    """
    Load project and context from backend.

    Parameters
    ----------
    client : Client
        Client to interact with backend.
    name : str
        The name of the project to load.

    Returns
    -------
    Project
        A Project instance with its context.

    """
    return get_project(client, name)


def create_project(
    name: str,
    source: str = None,
    description: str = None,
) -> Project:
    """
    Create a Project instance with the given parameters.

    Parameters
    ----------
    name : str
        The name of the project to be created.
    source : str, optional
        The source of the project (eg. git://repo-url).
    description : str, optional
        The description of the project.

    Returns
    -------
    Project
        A new Project instance with the specified parameters.

    """
    return Project(name, source, description)


def get_project(client: Client, name: str) -> Project:
    """
    Retrieves project details from the backend.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    name : str
        The name of the project.

    Returns
    -------
    Project
        An object that contains details about the specified project.

    Raises
    ------
    KeyError
        If the specified project does not exist.

    """
    name = get_id(name, client)
    r = client.get_object(API_READ.format(name))
    if "status" not in r:
        kwargs = {k: v for k, v in r.items() if k in OBJ_ATTR}
        project = Project(**kwargs)
        project.id = r["id"]
        return project
    raise KeyError(f"Project {name} does not exists.")


def delete_project(client: Client, name: str) -> None:
    """
    Delete a project.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    name : str
        The name of the project.

    Returns
    -------
    None
        This function does not return anything.
    """
    api = API_DELETE.format(get_id(name, client))
    delete_from_backend(client, api)


def import_project(file: str) -> Project:
    return file_importer(file, Project, OBJ_ATTR)


def export_project(project: Project, file: str) -> None:
    file_exporter(file, project.to_dict())


def get_id(name, client):
    for i in client.get_object(API_READ_ALL):
        if i["name"] == name:
            return i["id"]
    return name
