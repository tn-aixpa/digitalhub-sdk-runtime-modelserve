from sdk.entities.project.project import Project, ProjectMetadata, ProjectSpec
from sdk.entities.utils import file_importer
from sdk.client.factory import get_client
from sdk.utils.api import (
    API_READ_PROJECT,
    API_DELETE_PROJECT,
)


def new_project(
    name: str,
    description: str = None,
    context: str = "./",
    source: str = None,
    functions: list = None,
    artifacts: list = None,
    workflows: list = None,
    local: bool = False,
    embed: bool = False,
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
    local : bool, optional
        Flag to determine if object will be saved locally.
    embed : bool, optional
        Flag to determine if object related to project will be fully embedded or not.

    Returns
    -------
    Project
        A Project instance with its context.

    """
    if functions is None:
        functions = []
    if artifacts is None:
        artifacts = []
    if workflows is None:
        workflows = []
    meta = ProjectMetadata(name=name, description=description)
    spec = ProjectSpec(
        context=context,
        source=source,
        functions=functions,
        artifacts=artifacts,
        workflows=workflows,
    )
    obj = Project(name, metadata=meta, spec=spec, local=local, embed=embed)
    if not local:
        obj.save()
    return obj


def load_project(
    name: str,
    local: bool = False,
    filename: str = "project.yaml",
) -> Project:
    """
    Load project and context from backend.

    Parameters
    ----------
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
        client = get_client()
        return get_project(client, name)


def get_project(name: str, uuid: str = None) -> Project:
    """
    Retrieves project details from the backend.

    Parameters
    ----------
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
    api = API_READ_PROJECT.format(name)
    client = get_client()
    r = client.get_object(api)
    if "status" not in r:
        if "spec" not in r:
            r["spec"] = {}
            r["spec"]["source"] = r.get("source", None)
            r["spec"]["context"] = r.get("context", "./")
            r["spec"]["functions"] = r.get("functions", [])
            r["spec"]["artifacts"] = r.get("artifacts", [])
            r["spec"]["workflows"] = r.get("workflows", [])
        l = ["functions", "artifacts", "workflows", "source", "context"]
        r = {k: v for k, v in r.items() if k not in l}
        return Project(**r)
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
    return file_importer(
        file,
        Project,
    )


def delete_project(name: str, uuid: str = None) -> None:
    """
    Delete a project.

    Parameters
    ----------
    name : str
        The name of the project.

    Returns
    -------
    None
        This function does not return anything.
    """
    client = get_client()
    api = API_DELETE_PROJECT.format(name)
    return client.delete_object(api)
