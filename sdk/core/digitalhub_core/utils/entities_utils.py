"""
General utilities module.
"""
from __future__ import annotations

import re


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
    pattern: str = r"store://(?P<project>\w+)/(.*)/(?P<name>\w+):(?P<uuid>[A-Za-z0-9\-\_]+)"
    match = re.match(pattern, key)
    if match is None:
        raise ValueError("Invalid key format.")
    project = match.group("project")
    name = match.group("name")
    uuid = match.group("uuid")
    return project, name, uuid
