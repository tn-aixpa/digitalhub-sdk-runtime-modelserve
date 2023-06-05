"""
Project operations module.
"""
from sdk.client.factory import get_client
from sdk.entities.project.project import Project, ProjectMetadata, ProjectSpec
from sdk.entities.utils import file_importer
from sdk.entities.api import (
    API_DELETE_ALL,
    API_DELETE_PROJECT,
    API_READ_PROJECT,
    API_READ_PROJECT_OBJECTS,
    DTO_ARTF,
    DTO_DTIT,
    DTO_FUNC,
    DTO_WKFL,
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
    save: bool = False,
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
        Flag to determine if object has local execution.
    save : bool, optional
        Flag to determine if object will be saved.
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
    if save:
        if local:
            obj.export()
        else:
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
    r = get_client().get_object(api)

    spec = {}
    spec["source"] = r.get("source", None)
    spec["context"] = r.get("context", "./")
    spec["functions"] = r.get("functions", [])
    spec["artifacts"] = r.get("artifacts", [])
    spec["workflows"] = r.get("workflows", [])
    l = [
        "functions",
        "artifacts",
        "workflows",
        "source",
        "context",
        "metadata",
        "spec",
    ]
    r = {k: v for k, v in r.items() if k not in l}
    r["spec"] = spec
    return Project.from_dict(r)


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
    d = file_importer(file)
    return Project.from_dict(d)


def delete_project(name: str, delete_all: bool = False) -> None:
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
    responses = []
    # Delete all objects related to project
    if delete_all:
        for a in [DTO_ARTF, DTO_FUNC, DTO_WKFL]:
            api_obj = API_READ_PROJECT_OBJECTS.format(name, a)
            try:
                r = client.get_object(api_obj)
                for o in r:
                    api = API_DELETE_ALL.format(name, a, o["name"])
                    r = client.delete_object(api)
                    responses.append(r)
            except Exception:
                pass
    # Delete project
    try:
        api = API_DELETE_PROJECT.format(name)
        r = client.delete_object(api)
        responses.append(r)
    except Exception:
        pass
    return responses

