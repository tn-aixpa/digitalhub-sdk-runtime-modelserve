"""
Module for performing operations on functions.
"""
from __future__ import annotations

import typing

from digitalhub_core.context.builder import get_context
from digitalhub_core.entities.functions.entity import function_from_dict, function_from_parameters
from digitalhub_core.utils.api import api_ctx_delete, api_ctx_read, api_ctx_update
from digitalhub_core.utils.commons import FUNC
from digitalhub_core.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.functions.entity import Function


def create_function(**kwargs) -> Function:
    """
    Create a new object instance.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    Function
       Object instance.
    """
    return function_from_parameters(**kwargs)


def create_function_from_dict(obj: dict) -> Function:
    """
    Create a new Function instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create the Function from.

    Returns
    -------
    Function
        Function object.
    """
    return function_from_dict(obj)


def new_function(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    embedded: bool = True,
    source: str | None = None,
    **kwargs,
) -> Function:
    """
    Create a new Function instance and persist it to the backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        Identifier of the function.
    kind : str
        The type of the function.
    uuid : str
        UUID.
    description : str
        Description of the function.
    embedded : bool
        Flag to determine if object must be embedded in project.
    source : str
        Path to the function's source code on the local file system.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Function
       Object instance.
    """
    obj = create_function(
        project=project,
        name=name,
        kind=kind,
        uuid=uuid,
        description=description,
        source=source,
        embedded=embedded,
        **kwargs,
    )
    obj.save()
    return obj


def get_function(project: str, name: str, uuid: str | None = None) -> Function:
    """
    Get object from backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the function.
    uuid : str
        UUID.

    Returns
    -------
    Function
        Object instance.
    """
    api = api_ctx_read(project, FUNC, name, uuid=uuid)
    obj = get_context(project).read_object(api)
    return function_from_dict(obj)


def import_function(file: str) -> Function:
    """
    Get object from file.

    Parameters
    ----------
    file : str
        Path to the file.

    Returns
    -------
    Function
        Object instance.
    """
    obj = read_yaml(file)
    return function_from_dict(obj)


def delete_function(project: str, name: str, uuid: str | None = None) -> dict:
    """
    Delete function from the backend. If the uuid is not specified, delete all versions.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the function.
    uuid : str
        UUID.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_ctx_delete(project, FUNC, name, uuid=uuid)
    return get_context(project).delete_object(api)


def update_function(function: Function) -> dict:
    """
    Update a function.

    Parameters
    ----------
    function : Function
        The function to update.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_ctx_update(function.metadata.project, FUNC, function.metadata.name, uuid=function.id)
    return get_context(function.metadata.project).update_object(function.to_dict(), api)
