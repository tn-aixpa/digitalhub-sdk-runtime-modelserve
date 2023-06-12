"""
General utilities module.
"""
from uuid import uuid4


def get_uiid() -> str:
    """
    Create a uuid.

    Returns
    -------
    str
        The uuid.
    """
    return uuid4().hex
