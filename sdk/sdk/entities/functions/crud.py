"""
Module for performing operations on functions.
"""
from __future__ import annotations

import typing

from sdk.context.builder import get_context
from sdk.entities.functions.entity import function_from_dict, function_from_parameters
from sdk.utils.api import api_ctx_delete, api_ctx_read
from sdk.utils.commons import FUNC
from sdk.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from sdk.entities.functions.entity import Function


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
    description: str | None = None,
    kind: str | None = None,
    source: str | None = None,
    image: str | None = None,
    tag: str | None = None,
    handler: str | None = None,
    command: str | None = None,
    arguments: list | None = None,
    requirements: list | None = None,
    sql: str | None = None,
    embedded: bool = True,
    uuid: str | None = None,
    **kwargs,
) -> Function:
    """
    Create a new Function instance and persist it to the backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        Identifier of the Function.
    description : str
        Description of the Function.
    kind : str, default "job"
        The type of the Function.
    source : str
        Path to the Function's source code on the local file system.
    image : str
        Name of the Function's container image.
    tag : str
        Tag of the Function's container image.
    handler : str
        Function handler name.
    command : str
        Command to run inside the container.
    arguments : list
        List of arguments for the command.
    requirements : list
        List of requirements for the Function.
    sql : str
        SQL query.
    embedded : bool
        Flag to determine if object must be embedded in project.
    uuid : str
        UUID.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Function
       Object instance.

    Raises
    ------
    EntityError
        If the context local flag does not match the local flag of the function.
    """,
    obj = create_function(
        project=project,
        name=name,
        description=description,
        kind=kind,
        source=source,
        image=image,
        tag=tag,
        handler=handler,
        command=command,
        arguments=arguments,
        requirements=requirements,
        sql=sql,
        embedded=embedded,
        uuid=uuid,
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


def get_function_from_task(task: str) -> Function:
    """
    Get object from task.

    Parameters
    ----------
    task : str
        The task string.

    Returns
    -------
    Function
        Object instance.
    """
    splitted = task.split("/")
    project = splitted[2]
    fnc_name, fnc_version = splitted[-1].split(":")
    return get_function(project, fnc_name, uuid=fnc_version)


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
