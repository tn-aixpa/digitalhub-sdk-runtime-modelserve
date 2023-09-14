"""
Module for performing operations on functions.
"""
from __future__ import annotations

import typing

from sdk.context.factory import get_context
from sdk.entities.function.entity import function_from_dict, function_from_parameters
from sdk.utils.api import DTO_FUNC, api_ctx_delete, api_ctx_read
from sdk.utils.entities_utils import check_local_flag, save_or_export
from sdk.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from sdk.entities.function.entity import Function


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
    description: str = "",
    kind: str = "job",
    source: str | None = None,
    image: str | None = None,
    tag: str | None = None,
    handler: str | None = None,
    command: str | None = None,
    requirements: list | None = None,
    sql: str | None = None,
    local: bool = False,
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
    requirements : list
        List of requirements for the Function.
    sql : str
        SQL query.
    local : bool
        Flag to determine if object will be exported to backend.
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
    """
    check_local_flag(project, local)
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
        requirements=requirements,
        sql=sql,
        local=local,
        embedded=embedded,
        uuid=uuid,
        **kwargs,
    )
    save_or_export(obj, local)
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
    api = api_ctx_read(project, DTO_FUNC, name, uuid=uuid)
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
    api = api_ctx_delete(project, DTO_FUNC, name, uuid=uuid)
    return get_context(project).delete_object(api)
