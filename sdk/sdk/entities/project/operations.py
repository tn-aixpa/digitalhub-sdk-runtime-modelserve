from sdk.entities.project.project import Project
from sdk.entities.utils import file_importer, file_exporter, delete_from_backend
from sdk.client.client import Client


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
    """
    Import an Project object from a file using the specified file path.

    Parameters
    ----------
    file : str
        The absolute or relative path to the file containing the Project object.

    Returns
    -------
    Project
        The Project object imported from the file using the specified path.

    """
    return file_importer(file, Project, OBJ_ATTR)


def export_project(project: Project, file: str) -> None:
    """
    Export the specified Project object to a file in the specified location.

    Parameters
    ----------
    project : Project
        The Project object to be exported.
    file : str
        The absolute or relative path to the file in which the Project object
        will be exported.

    Returns
    -------
    None
    """
    file_exporter(file, project.to_dict())


def get_id(name, client):
    for i in client.get_object(API_READ_ALL):
        if i["name"] == name:
            return i["id"]
    return name
