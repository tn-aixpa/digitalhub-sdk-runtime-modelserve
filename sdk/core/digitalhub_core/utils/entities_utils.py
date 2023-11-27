"""
General utilities module.
"""
from __future__ import annotations


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
    try:
        # Remove "store://" from the key
        key = key.replace("store://", "")
        # Split the key into parts
        parts = key.split("/")
        project = parts[0]
        # The name and uuid are separated by a colon in the last part
        name, uuid = parts[-1].split(":")
        return project, name, uuid
    except Exception as e:
        raise ValueError("Invalid key format.") from e
