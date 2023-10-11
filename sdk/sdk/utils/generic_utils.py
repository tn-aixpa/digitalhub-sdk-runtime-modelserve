"""
General utilities module.
"""
from __future__ import annotations

import base64
from datetime import datetime
from uuid import uuid4

from sdk.utils.io_utils import read_text


def build_uuid(uuid: str | None = None) -> str:
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
    return str(uuid4())


def get_timestamp() -> str:
    """
    Get the current timestamp timezoned.

    Returns
    -------
    str
        The current timestamp.
    """
    return datetime.now().astimezone().isoformat()


def decode_string(string: str) -> str:
    """
    Decode a string from base64.

    Parameters
    ----------
    string : str
        The string to decode.

    Returns
    -------
    str
        The string decoded from base64.
    """
    return base64.b64decode(string).decode()


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
