from sdk.entities.project.project import Project
from sdk.entities.utils import file_importer, delete_from_backend
from sdk.client.client import Client
from sdk.utils.common import (
    API_READ_LATEST,
    API_READ_VERSION,
    API_DELETE_VERSION,
    API_DELETE_ALL,
    DTO_PROJ,
)


OBJ_ATTR = [
    "name",
    "source",
    "description",
    "functions",
    "artifacts",
    "workflows",
]


def new_project(
    name: str,
    source: str = None,
    description: str = None,
    client: Client = None,
    local: bool = False,
    filename: str = None,
) -> Project:
    """
    Create a new project and an execution context.

    Parameters
    ----------
    name : str
        The name of the project to load.
    source : str, optional
        The source of the project (eg. remote git://repo-url, or local "./").
    description : str, optional
        The description of the project.
    client : Client, optional
        A Client object to interact with backend.
    local : bool, optional
        Flag to determine if object wil be saved locally.
    filename : str, optional
        Filename to export object.

    Returns
    -------
    Project
        A Project instance with its context.

    """
    obj = Project(name, source, description)
    if local:
        obj.export(filename)
    else:
        obj.save(client)
    return obj


def load_project(
    name: str,
    client: Client = None,
    local: bool = False,
    filename: str = "project.yaml",
) -> Project:
    """
    Load project and context from backend.

    Parameters
    ----------
    client : Client
        Client to interact with backend.
    name : str
        The name of the project to load from backend.
    filename : str
        Path to file where to load project from.
    local : bool
        Flag to determine if project wil be executed locally.

    Returns
    -------
    Project
        A Project instance with its context.

    """
    if local:
        return import_project(filename)
    else:
        return get_project(client, name)


def get_project(client: Client, name: str, uuid: str = None) -> Project:
    """
    Retrieves project details from the backend.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    name : str
        The name of the project.
    uuid : str, optional
        UUID of project specific version.

    Returns
    -------
    Project
        An object that contains details about the specified project.

    Raises
    ------
    KeyError
        If the specified project does not exist.

    """
    if uuid is not None:
        api = API_READ_VERSION.format(name, DTO_PROJ, name, uuid)
    else:
        api = API_READ_LATEST.format(name, DTO_PROJ, name)

    r = client.get_object(api)
    if "status" not in r:
        kwargs = {k: v for k, v in r.items() if k in OBJ_ATTR}
        project = Project(**kwargs)
        project.id = r["id"]
        return project
    raise KeyError(f"Project {name} does not exists.")


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


def delete_project(client: Client, name: str, uuid: str = None) -> None:
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
    if uuid is not None:
        api = API_DELETE_VERSION.format(name, DTO_PROJ, name, uuid)
    else:
        api = API_DELETE_ALL.format(name, DTO_PROJ, name)
    return delete_from_backend(client, api)
