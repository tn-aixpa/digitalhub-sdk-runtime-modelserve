"""
Project operations module.
"""
from sdk.utils.api import (
    DTO_ARTF,
    DTO_DTIT,
    DTO_FUNC,
    DTO_WKFL,
    delete_api,
    delete_api_project,
    read_api_project,
)
from sdk.entities.project.entity import Project, ProjectMetadata, ProjectSpec
from sdk.utils.factories import delete_context, get_client
from sdk.utils.io_utils import read_yaml


def new_project(
    name: str,
    description: str = None,
    context: str = None,
    source: str = None,
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
    local : bool, optional
        Flag to determine if project wil be executed locally.

    Returns
    -------
    Project
        A Project instance with its context.

    """
    meta = ProjectMetadata(name=name, description=description)
    spec = ProjectSpec(
        context=context,
        source=source,
        functions=[],
        artifacts=[],
        workflows=[],
        dataitems=[],
    )
    obj = Project(name, metadata=meta, spec=spec, local=local)
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
        A Project instance with setted context.

    """
    if local:
        return import_project(filename)
    return get_project(name)


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
    obj_be = get_client().get_object(api)

    # Extract spec
    spec = {}
    spec["source"] = obj_be.get("source", None)
    spec["context"] = obj_be.get("context", "./")
    spec["functions"] = obj_be.get("functions", [])
    spec["artifacts"] = obj_be.get("artifacts", [])
    spec["workflows"] = obj_be.get("workflows", [])
    spec["dataitems"] = obj_be.get("dataitems", [])

    # Filter out spec from object
    fields = [
        "functions",
        "artifacts",
        "workflows",
        "source",
        "context",
        "metadata",
        "spec",
    ]

    # Set spec for new object and create Project instance
    obj = {k: v for k, v in obj_be.items() if k not in fields}
    obj["spec"] = spec
    return Project.from_dict(obj)


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
    obj = read_yaml(file)
    return Project.from_dict(obj)


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
        for dto in [DTO_ARTF, DTO_FUNC, DTO_WKFL, DTO_DTIT]:
            api_proj = read_api_project(name, dto)
            try:
                objs = client.get_object(api_proj)
                for obj in objs:
                    api = delete_api(name, dto, obj["name"])
                    responses.append(client.delete_object(api))
            except Exception:
                ...

    # Delete project
    try:
        api = delete_api_project(name)
        responses.append(client.delete_object(api))
    except Exception:
        ...

    delete_context(name)

    return responses
