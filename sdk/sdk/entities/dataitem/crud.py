"""
Module for performing operations on Dataitem objects.
"""
from __future__ import annotations

import typing

from sdk.entities.dataitem.entity import dataitem_from_parameters, dataitem_from_dict
from sdk.entities.utils.utils import check_local_flag, save_or_export
from sdk.utils.api import DTO_DTIT, api_ctx_delete, api_ctx_read
from sdk.utils.factories import get_context
from sdk.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from sdk.entities.dataitem.entity import Dataitem


def create_dataitem(
    project: str,
    name: str,
    description: str = "",
    kind: str = "dataitem",
    key: str = None,
    path: str = None,
    local: bool = False,
    embedded: bool = False,
    uuid: str = None,
) -> Dataitem:
    """
    Create a new data item with the provided parameters.

    Parameters
    ----------
    project : str
        Name of the project associated with the data item.
    name : str
        Identifier of the data item.
    description : str, optional
        Description of the data item.
    kind : str, optional
        The type of the data item.
    key : str
        Representation of data item like store://etc..
    path : str
        Path to the data item on local file system or remote storage.
    local : bool, optional
        Flag to determine if object has local execution.
    embedded : bool, optional
        Flag to determine if object must be embedded in project.
    uuid : str, optional
        UUID.

    Returns
    -------
    Dataitem
        An instance of the Dataitem class representing the specified data item.
    """
    return dataitem_from_parameters(
        project=project,
        name=name,
        description=description,
        kind=kind,
        key=key,
        path=path,
        local=local,
        embedded=embedded,
        uuid=uuid,
    )


def create_dataitem_from_dict(obj: dict) -> Dataitem:
    """
    Create a new Dataitem instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create the Dataitem from.

    Returns
    -------
    Dataitem
        Dataitem object.
    """
    return dataitem_from_dict(obj)


def new_dataitem(
    project: str,
    name: str,
    description: str = "",
    kind: str = "dataitem",
    key: str = None,
    path: str = None,
    local: bool = False,
    embedded: bool = False,
    uuid: str = None,
) -> Dataitem:
    """
    Create a new Dataitem instance with the given parameters.

    Parameters
    ----------
    project : str
        Name of the project associated with the dataitem.
    name : str
        Identifier of the dataitem.
    description : str, optional
        Description of the dataitem.
    kind : str, optional
        The type of the dataitem.
    key : str, optional
        Representation of the dataitem, e.g. store://etc.
    path : str, optional
        Path to the dataitem on local file system or remote storage.
    local : bool, optional
        Flag to determine if object has local execution.
    embedded : bool, optional
        Flag to determine if object must be embedded in project.
    uuid : str, optional
        UUID.

    Returns
    -------
    Dataitem
        Instance of the Dataitem class representing the specified dataitem.
    """
    check_local_flag(project, local)
    obj = create_dataitem(
        project=project,
        name=name,
        description=description,
        kind=kind,
        key=key,
        path=path,
        local=local,
        embedded=embedded,
        uuid=uuid,
    )
    save_or_export(obj, local)
    return obj


def get_dataitem(project: str, name: str, uuid: str = None) -> Dataitem:
    """
    Retrieve dataitem details from the backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the dataitem.
    uuid : str, optional
        UUID of dataitem specific version.

    Returns
    -------
    Dataitem
        An object that contains details about the specified dataitem.


    """
    api = api_ctx_read(project, DTO_DTIT, name, uuid=uuid)
    obj = get_context(project).read_object(api)
    return dataitem_from_dict(obj)


def import_dataitem(file: str) -> Dataitem:
    """
    Import a Dataitem object from a file using the specified file path.

    Parameters
    ----------
    file : str
        The absolute or relative path to the file containing the Dataitem object.

    Returns
    -------
    Dataitem
        The Dataitem object imported from the file using the specified path.

    """
    obj = read_yaml(file)
    return dataitem_from_dict(obj)


def delete_dataitem(project: str, name: str, uuid: str = None) -> None:
    """
    Delete dataitem from the backend. If the uuid is not specified, delete all versions.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the dataitem.
    uuid : str, optional
        UUID of dataitem specific version.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_ctx_delete(project, DTO_DTIT, name, uuid=uuid)
    return get_context(project).delete_object(api)
