"""
Module for performing operations on Dataitem objects.
"""
from __future__ import annotations

import typing

from sdk.context.factory import get_context
from sdk.entities.dataitem.entity import dataitem_from_dict, dataitem_from_parameters
from sdk.utils.api import api_ctx_delete, api_ctx_read
from sdk.utils.commons import DTIT
from sdk.utils.entities_utils import check_local_flag, parse_entity_key, save_or_export
from sdk.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from sdk.entities.dataitem.entity import Dataitem


def create_dataitem(**kwargs) -> Dataitem:
    """
    Create a new data item with the provided parameters.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    Dataitem
        Object instance.
    """
    return dataitem_from_parameters(**kwargs)


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
    kind: str | None = None,
    key: str | None = None,
    path: str | None = None,
    local: bool = False,
    embedded: bool = True,
    uuid: str | None = None,
    **kwargs,
) -> Dataitem:
    """
    Create a new object instance.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        Identifier of the dataitem.
    description : str
        Description of the dataitem.
    kind : str
        The type of the dataitem.
    key : str
        Representation of the dataitem, e.g. store://etc.
    path : str
        Path to the dataitem on local file system or remote storage.
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
    Dataitem
       Object instance.
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
        **kwargs,
    )
    save_or_export(obj, local)
    return obj


def get_dataitem(project: str, name: str, uuid: str | None = None) -> Dataitem:
    """
    Get object from backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the dataitem.
    uuid : str
        UUID.

    Returns
    -------
    Dataitem
        Object instance.

    """
    api = api_ctx_read(project, DTIT, name, uuid=uuid)
    obj = get_context(project).read_object(api)
    return dataitem_from_dict(obj)


def get_dataitem_from_key(key: str) -> Dataitem:
    """
    Get dataitem from key.

    Parameters
    ----------
    key : str
        Key of the dataitem.
        It's format is store://<project>/dataitems/<kind>/<name>:<uuid>.
    """
    project, name, uuid = parse_entity_key(key)
    return get_dataitem(project, name, uuid)


def import_dataitem(file: str) -> Dataitem:
    """
    Get object from file.

    Parameters
    ----------
    file : str
        Path to the file.

    Returns
    -------
    Dataitem
        Object instance.
    """
    obj = read_yaml(file)
    return dataitem_from_dict(obj)


def delete_dataitem(project: str, name: str, uuid: str | None = None) -> dict:
    """
    Delete dataitem from the backend. If the uuid is not specified, delete all versions.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the dataitem.
    uuid : str
        UUID.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_ctx_delete(project, DTIT, name, uuid=uuid)
    return get_context(project).delete_object(api)
