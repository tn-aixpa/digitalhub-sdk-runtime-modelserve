"""
Project module.
"""

from sdk.client.client import Client
from sdk.utils.utils import write_yaml, read_yaml


# All'inizio: client.new_project(), client.load_project() ....
# project = dhub.new_project("test") -> return obj project + context
# ==
# project = dhub.load_project("test", client=client) -> return obj project + context

# mi aspetto di potre fare
# project.get_artifact(),  set_function(), run_function(), save() etc.

# non mi aspetto project.delete() perche operazione su struttura dati

# struct_project = dhub.get_project() -> struttura dati da backend (obj)
# struct_project = dhub.import_project() -> struttura dati da file (obj)

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
OBJ_BARE_ATTR = [
    "name",
    "source",
    "description",
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
        source: str = None,
        description: str = None,
    ) -> None:
        """Initialize the Project instance."""
        self.name = name
        self.source = source
        self.description = description
        self.functions = []
        self.artifacts = []
        self.workflows = []
        self.id = None

    @classmethod
    def new(
        cls,
        client: Client,
        name: str,
        source: str = None,
        description: str = None,
    ) -> "Project":
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
        obj = cls(name, source, description)
        obj.save(client)
        return obj

    @classmethod
    def load(cls, client: Client, name: str) -> "Project":
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
        name = get_id(name, client)
        r = client.get_object(API_READ.format(name))
        kwargs = {k: v for k, v in r.items() if k in OBJ_ATTR}
        project = cls(**kwargs)
        project.id = r["id"]
        return project

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

    def set_artifact(self, artifact: "Artifact", client: Client) -> dict:
        return artifact.save(client)

    def to_dict(self) -> dict:
        """
        Return object to dict.

        Returns
        -------
        dict
            A dictionary containing the attributes of the Project instance.

        """
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def __repr__(self) -> str:
        """
        Return string representation of the project object.

        Returns
        -------
        str
            A string representing the Project instance.

        """
        return str(self.to_dict())


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
        kwargs = {k: v for k, v in r.items() if k in OBJ_BARE_ATTR}
        project = Project(**kwargs)
        project.id = r["id"]
        project.artifacts = r["artifacts"]
        project.functions = r["functions"]
        project.workflows = r["workflows"]
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

    Raises
    ------
    Any exceptions raised by the client object's delete_object method.
    """
    name = get_id(name, client)
    client.delete_object(API_DELETE.format(name))


def import_project(file: str) -> Project:
    dict_ = read_yaml(file)
    kwargs = {k: v for k, v in dict_.items() if k in OBJ_BARE_ATTR}
    project = Project(**kwargs)
    try:
        project.id = dict_["id"]
    except:
        ...
    return project


def export_project(project: Project, file: str) -> None:
    data = project.to_dict()
    write_yaml(data, file)


def get_id(name, client):
    for i in client.get_object(API_READ_ALL):
        if i["name"] == name:
            return i["id"]
    return name
