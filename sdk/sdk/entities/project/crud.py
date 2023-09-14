"""
Project operations module.
"""
from __future__ import annotations

import typing

from sdk.client.factory import get_client
from sdk.context.factory import delete_context
from sdk.entities.project.entity import project_from_dict, project_from_parameters
from sdk.utils.api import (
    DTO_ARTF,
    DTO_DTIT,
    DTO_FUNC,
    DTO_PROJ,
    DTO_WKFL,
    api_base_delete,
    api_base_read,
    api_ctx_delete,
)
from sdk.utils.entities_utils import save_or_export
from sdk.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from sdk.entities.project.entity import Project


def create_project(**kwargs) -> Project:
    """
    Create a new project.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    Project
        A Project instance.
    """
    return project_from_parameters(**kwargs)


def new_project(
    name: str,
    description: str = "",
    context: str | None = None,
    source: str | None = None,
    local: bool = False,
    uuid: str | None = None,
) -> Project:
    """
    Create a new project and an execution context.

    Parameters
    ----------
    name : str
        Name of the project.
    description : str
        The description of the project.
    context : str
        The path to the project's execution context.
    source : str
        The path to the project's source code.
    local : bool
        Flag to determine if project wil be executed locally.
    uuid : str
        UUID.

    Returns
    -------
    Project
        A Project instance with its context.
    """
    obj = create_project(
        name=name,
        description=description,
        context=context,
        source=source,
        local=local,
        uuid=uuid,
    )
    save_or_export(obj, local)
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
        Name of the project.
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
        The name or UUID.

    Returns
    -------
    Project
        Object instance.
    """
    api = api_base_read(DTO_PROJ, name)
    obj_be = get_client().read_object(api)

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
    return project_from_dict(obj)


def import_project(file: str) -> Project:
    """
    Import an Project object from a file using the specified file path.

    Parameters
    ----------
    file : str
        Path to the file.

    Returns
    -------
    Project
        Object instance.
    """
    obj = read_yaml(file)
    return project_from_dict(obj)


def delete_project(name: str, delete_all: bool = False) -> list[dict]:
    """
    Delete a project.

    Parameters
    ----------
    name : str
        Name of the project.

    Returns
    -------
    dict
        Response from backend.
    """
    client = get_client()
    responses = []

    # Delete all objects related to project -> must be done by backend
    if delete_all:
        for dto in [DTO_ARTF, DTO_FUNC, DTO_WKFL, DTO_DTIT]:
            api_proj = f"/api/v1/{DTO_PROJ}/{name}/{dto}"
            try:
                objs = client.read_object(api_proj)
                for obj in objs:
                    api = api_ctx_delete(name, dto, obj["name"])
                    responses.append(client.delete_object(api))
            except Exception:
                ...

    # Delete project
    try:
        api = api_base_delete(DTO_PROJ, name)
        responses.append(client.delete_object(api))
    except Exception:
        ...

    delete_context(name)

    return responses
