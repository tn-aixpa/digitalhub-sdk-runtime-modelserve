"""
Function operations module.
"""
from sdk.entities.function.entity import Function, FunctionMetadata, FunctionSpec
from sdk.utils.api import DTO_FUNC, api_ctx_delete, api_ctx_read
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context
from sdk.utils.io_utils import read_yaml


def new_function(
    project: str,
    name: str,
    description: str = None,
    kind: str = None,
    source: str = None,
    image: str = None,
    tag: str = None,
    handler: str = None,
    command: str = None,
    requirements: list = None,
    local: bool = False,
    embed: bool = False,
) -> Function:
    """
    Create a Function instance with the given parameters.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        Identifier of the Function.
    description : str, optional
        Description of the Function.
    kind : str, optional
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
    embed : bool, optional
        Flag to determine if object must be embedded in project.

    Returns
    -------
    Function
        Instance of the Function class representing the specified function.
    """
    context = get_context(project)
    if context.local != local:
        raise EntityError("Context local flag does not match local flag of function")
    meta = FunctionMetadata(name=name, description=description)
    spec = FunctionSpec(
        source=source,
        image=image,
        tag=tag,
        handler=handler,
        command=command,
        requirements=requirements,
    )
    obj = Function(
        project=project,
        name=name,
        kind=kind,
        metadata=meta,
        spec=spec,
        local=local,
        embed=embed,
    )
    if local:
        obj.export()
    else:
        obj.save()
    return obj


def get_function(project: str, name: str, uuid: str = None) -> Function:
    """
    Retrieves function details from the backend.

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

    Raises
    ------
    KeyError
        If the specified function does not exist.

    """
    context = get_context(project)
    api = api_ctx_read(project, DTO_FUNC, name, uuid=uuid)
    obj = context.client.get_object(api)
    return Function.from_dict(obj)


def import_function(file: str) -> Function:
    """
    Import an Function object from a file using the specified file path.

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
    return Function.from_dict(obj)


def delete_function(project: str, name: str, uuid: str = None) -> None:
    """
    Delete function from the backend. If the uuid is not specified, delete all versions.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    project : str
        Name of the project.
    name : str
        The name of the function.
    uuid : str, optional
        UUID of function specific version.

    Returns
    -------
    None
        This function does not return anything.
    """
    context = get_context(project)
    api = api_ctx_delete(project, DTO_FUNC, name, uuid=uuid)
    return context.client.delete_object(api)
