"""
Project operations module.
"""
from __future__ import annotations

import typing

from digitalhub_core.client.builder import get_client
from digitalhub_core.context.builder import delete_context
from digitalhub_core.entities.projects.entity import project_from_dict, project_from_parameters
from digitalhub_core.utils.api import api_base_delete, api_base_read, api_base_update
from digitalhub_core.utils.commons import PROJ
from digitalhub_core.utils.exceptions import BackendError, EntityError
from digitalhub_core.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.projects.entity import Project


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
    uuid: str | None = None,
    description: str | None = None,
    local: bool = False,
    context: str = "",
    source: str = "",
    **kwargs,
) -> Project:
    """
    Create project.

    Parameters
    ----------
    name : str
        Identifier of the project.
    kind : str
        The type of the project.
    uuid : str
        UUID.
    description : str
        Description of the project.
    local : bool
        Flag to determine if object will be exported to backend.
    context : str
        The context of the project.
    source : str
        The source of the project.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Project
        Project object.
    """
    obj = create_project(
        name=name,
        kind="project",
        uuid=uuid,
        description=description,
        local=local,
        context=context,
        source=source,
        **kwargs,
    )
    obj.save()
    return obj


def load_project(name: str | None = None, filename: str | None = None, local: bool = False) -> Project:
    """
    Load project and context from backend or file.

    Parameters
    ----------
    name : str
        Name of the project.
    filename : str
        Path to file where to load project from.
    local : bool
        Flag to determine if backend is local.

    Returns
    -------
    Project
        A Project instance with setted context.
    """
    if name is not None:
        return get_project(name, local)
    if filename is not None:
        return import_project(filename, local)
    raise EntityError("Either name or filename must be provided.")


def get_or_create_project(
    name: str,
    local: bool = False,
    **kwargs,
) -> Project:
    """
    Get or create a project.

    Parameters
    ----------
    name : str
        Name of the project.
    local : bool
        Flag to determine if backend is local.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Project
        A Project instance.
    """
    try:
        return get_project(name, local)
    except BackendError:
        return new_project(name, local=local, **kwargs)


def get_project(name: str, local: bool = False) -> Project:
    """
    Retrieves project details from the backend.

    Parameters
    ----------
    name : str
        The name or UUID.
    local : bool
        Flag to determine if backend is local.

    Returns
    -------
    Project
        Object instance.
    """
    api = api_base_read(PROJ, name)
    client = get_client(local)
    obj = client.read_object(api)
    return project_from_dict(obj)


def import_project(file: str, local: bool = False) -> Project:
    """
    Import an Project object from a file using the specified file path.

    Parameters
    ----------
    file : str
        Path to the file.
    local : bool
        Flag to determine if backend is local.

    Returns
    -------
    Project
        Object instance.
    """
    obj = read_yaml(file)
    obj["local"] = local
    return project_from_dict(obj)


def delete_project(name: str, local: bool = False) -> list[dict]:
    """
    Delete a project.

    Parameters
    ----------
    name : str
        Name of the project.
    local : bool
        Flag to determine if backend is local.

    Returns
    -------
    dict
        Response from backend.
    """
    client = get_client(local)
    api = api_base_delete(PROJ, name)
    response = client.delete_object(api)
    delete_context(name)
    return response


def update_project(project: Project, local: bool = False) -> dict:
    """
    Update a project.

    Parameters
    ----------
    project : Project
        The project to update.
    local : bool
        Flag to determine if backend is local.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_base_update(PROJ, project.metadata.name)
    client = get_client(local)
    return client.update_object(project.to_dict(), api)
