"""
Module for performing operations on functions.
"""
from __future__ import annotations

import typing

from sdk.entities.function.entity import function_from_dict, function_from_parameters
from sdk.entities.utils.utils import check_local_flag, save_or_export
from sdk.utils.api import DTO_FUNC, api_ctx_delete, api_ctx_read
from sdk.utils.factories import get_context
from sdk.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from sdk.entities.function.entity import Function


def create_function(
    project: str,
    name: str,
    description: str = "",
    kind: str = "job",
    source: str = None,
    image: str = None,
    tag: str = None,
    handler: str = None,
    command: str = None,
    requirements: list = None,
    local: bool = False,
    embedded: bool = False,
    uuid: str = None,
) -> Function:
    """
    Create a new Function instance with the given parameters.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        Identifier of the Function.
    description : str, optional
        Description of the Function.
    kind : str, optional, default "job"
        The type of the Function.
    source : str, optional
        Path to the Function's source code on the local file system.
    image : str, optional
        Name of the Function's container image.
    tag : str, optional
        Tag of the Function's container image.
    handler : str, optional
        Function handler name.
    command : str, optional
        Command to run inside the container.
    requirements : list, optional
        List of requirements for the Function.
    local : bool, optional
        Flag to determine if object has local execution.
    embedded : bool, optional
        Flag to determine if object must be embedded in project.
    uuid : str, optional
        UUID.

    Returns
    -------
    Function
        Instance of the Function class representing the specified function.

    """
    return function_from_parameters(
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
        local=local,
        embedded=embedded,
        uuid=uuid,
    )


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
    source: str = None,
    image: str = None,
    tag: str = None,
    handler: str = None,
    command: str = None,
    requirements: list = None,
    local: bool = False,
    embedded: bool = False,
    uuid: str = None,
) -> Function:
    """
    Create a new Function instance and persist it to the backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        Identifier of the Function.
    description : str, optional
        Description of the Function.
    kind : str, optional, default "job"
        The type of the Function.
    source : str, optional
        Path to the Function's source code on the local file system.
    image : str, optional
        Name of the Function's container image.
    tag : str, optional
        Tag of the Function's container image.
    handler : str, optional
        Function handler name.
    command : str, optional
        Command to run inside the container.
    requirements : list, optional
        List of requirements for the Function.
    local : bool, optional
        Flag to determine if object has local execution.
    embedded : bool, optional
        Flag to determine if object must be embedded in project.
    uuid : str, optional
        UUID.

    Returns
    -------
    Function
        Instance of the Function class representing the specified function.

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
        local=local,
        embedded=embedded,
        uuid=uuid,
    )
    save_or_export(obj, local)
    return obj


def get_function(project: str, name: str, uuid: str = None) -> Function:
    """
    Retrieve function details from the backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the function.
    uuid : str, optional
        UUID of function specific version.

    Returns
    -------
    Function
        An object that contains details about the specified function.

    """
    api = api_ctx_read(project, DTO_FUNC, name, uuid=uuid)
    obj = get_context(project).read_object(api)
    return function_from_dict(obj)


def import_function(file: str) -> Function:
    """
    Import a Function object from a file using the specified file path.

    Parameters
    ----------
    file : str
        The absolute or relative path to the file containing the Function object.

    Returns
    -------
    Function
        The Function object imported from the file using the specified path.
    """
    obj = read_yaml(file)
    return function_from_dict(obj)


def delete_function(project: str, name: str, uuid: str = None) -> None:
    """
    Delete function from the backend. If the uuid is not specified, delete all versions.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the function.
    uuid : str, optional
        UUID of function specific version.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_ctx_delete(project, DTO_FUNC, name, uuid=uuid)
    return get_context(project).delete_object(api)
