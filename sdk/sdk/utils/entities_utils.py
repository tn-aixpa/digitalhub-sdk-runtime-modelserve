"""
General utilities module.
"""
from __future__ import annotations

import re
import typing

from sdk.context.factory import get_context
from sdk.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from sdk.entities.base.entity import Entity


def check_local_flag(project: str, local: bool) -> None:
    """
    Checks if the local flag of the context matches the local flag of the object.

    Parameters
    ----------
    project : str
        Name of the project.
    local : bool
        Flag to determine if object will be exported to backend.

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
        Flag to determine if object will be exported to backend.

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
