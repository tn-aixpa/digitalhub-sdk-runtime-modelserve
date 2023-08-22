"""
General utilities module.
"""
from __future__ import annotations

import base64
import re
import typing
from uuid import uuid4

from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context
from sdk.utils.io_utils import read_text

if typing.TYPE_CHECKING:
    from sdk.entities.base.entity import Entity


def get_uiid(uuid: str | None = None) -> str:
    """
    Create a uuid if not given

    Parameters
    ----------
    uuid : str
        UUID. Optional.

    Returns
    -------
    str
        The uuid.
    """
    if uuid is not None:
        return uuid
    return uuid4().hex


def encode_string(string: str) -> str:
    """
    Encode a string in base64.

    Parameters
    ----------
    string : str
        The string to encode.

    Returns
    -------
    str
        The string encoded in base64.
    """
    return base64.b64encode(string.encode()).decode()


def encode_source(path: str) -> str:
    """
    Read a file and encode in base64 the content.

    Parameters
    ----------
    path : str
        The file path to read.

    Returns
    -------
    str
        The file content encoded in base64.
    """
    return encode_string(read_text(path))


def check_local_flag(project: str, local: bool) -> None:
    """
    Checks if the local flag of the context matches the local flag of the object.

    Parameters
    ----------
    project : str
        Name of the project.
    local : bool
        Flag to determine if object has local execution.

    Raises
    ------
    EntityError
        If the local flag of the context does not match the local flag of the object.
    """
    if get_context(project).local != local:
        raise EntityError("Context local flag does not match local flag of object")


def save_or_export(obj: Entity, local: bool) -> None:
    """
    Save or export the object based on local flag.

    Parameters
    ----------
    obj : object
        The object to save or export.
    local : bool
        Flag to determine if object has local execution.

    Returns
    -------
    None
    """
    if local:
        obj.export()
    else:
        obj.save()


def parse_entity_key(key: str) -> tuple[str, str, str]:
    """
    Parse the entity key.

    Parameters
    ----------
    key : str
        The entity key.

    Returns
    -------
    tuple[str, str, str]
        The project, the name and the uuid of the entity.
    """
    pattern: str = (
        r"store://(?P<project>\w+)/(.*)/(?P<name>\w+):(?P<uuid>[A-Za-z0-9\-\_]+)"
    )
    match = re.match(pattern, key)
    if match is None:
        raise ValueError("Invalid key format.")
    project = match.group("project")
    name = match.group("name")
    uuid = match.group("uuid")
    return project, name, uuid
