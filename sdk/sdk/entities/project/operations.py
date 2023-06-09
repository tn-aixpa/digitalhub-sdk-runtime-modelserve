"""
Project operations module.
"""
from sdk.entities.api import (
    DTO_ARTF,
    DTO_DTIT,
    DTO_FUNC,
    DTO_WKFL,
    delete_api,
    delete_api_project,
    read_api_project,
)
from sdk.entities.project.project import Project, ProjectMetadata, ProjectSpec
from sdk.utils.context_utils import delete_context, get_client, set_context
from sdk.utils.io_utils import file_importer


def new_project(
    name: str,
    description: str = None,
    context: str = None,
    source: str = None,
    functions: list = None,
    artifacts: list = None,
    workflows: list = None,
    dataitems: list = None,
    local: bool = False,
) -> Project:
    """
    Create a new project and an execution context.

    Parameters
    ----------
    name : str
        The name of the project to load.
    description : str, optional
        The description of the project.
    context : str, optional
        The path to the project's execution context.
    source : str, optional
        The path to the project's source code.
    functions : list, optional
        A list of functions assigned to the project.
    artifacts : list, optional
        A list of artifacts assigned to the project.
    workflows : list, optional
        A list of workflows assigned to the project.
    dataitems : list, optional
        A list of dataitems assigned to the project.
    local : bool, optional
        Flag to determine if project wil be executed locally.

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
    if dataitems is None:
        dataitems = []
    meta = ProjectMetadata(name=name, description=description)
    spec = ProjectSpec(
        context=context,
        source=source,
        functions=functions,
        artifacts=artifacts,
        workflows=workflows,
        dataitems=dataitems,
    )
    obj = Project(name, metadata=meta, spec=spec, local=local)
    set_context(obj)
    if local:
        obj.export()
    else:
        obj.save()
    return obj


def load_project(
    name: str,
    filename: str = "project.yaml",
    local: bool = False,
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
        obj = import_project(filename)
    else:
        client = get_client()
        obj = get_project(client, name)
    set_context(obj)
    return obj


def get_project(name: str) -> Project:
    """
    Retrieves project details from the backend.

    Parameters
    ----------
    name : str
        The name or UUID of the project.

    Returns
    -------
    Project
        An object that contains details about the specified project.

    """
    api = read_api_project(name)
    r = get_client().get_object(api)
    spec = {}
    spec["source"] = r.get("source", None)
    spec["context"] = r.get("context", "./")
    spec["functions"] = r.get("functions", [])
    spec["artifacts"] = r.get("artifacts", [])
    spec["workflows"] = r.get("workflows", [])
    spec["dataitems"] = r.get("dataitems", [])
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
    obj = Project.from_dict(r)
    set_context(obj)
    return obj


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
    obj = Project.from_dict(d)
    set_context(obj)
    return obj


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
    # Delete all objects related to project -> must be done by backend
    if delete_all:
        for a in [DTO_ARTF, DTO_FUNC, DTO_WKFL, DTO_DTIT]:
            api_obj = read_api_project(name, a)
            try:
                r = client.get_object(api_obj)
                for o in r:
                    api = delete_api(name, a, o["name"])
                    r = client.delete_object(api)
                    responses.append(r)
            except Exception:
                pass
    # Delete project
    try:
        api = delete_api_project(name)
        r = client.delete_object(api)
        responses.append(r)
    except Exception:
        pass

    delete_context(name)

    return responses
