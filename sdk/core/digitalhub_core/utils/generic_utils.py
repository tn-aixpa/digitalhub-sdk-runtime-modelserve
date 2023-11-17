"""
General utilities module.
"""
from __future__ import annotations

import base64
import os
from datetime import datetime
from uuid import uuid4

from digitalhub_core.utils.io_utils import read_text


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


def set_dhub_env(
    endpoint: str | None = None,
    user: str | None = None,
    password: str | None = None,
    token: str | None = None,
) -> None:
    """
    Function to set environment variables for DHub Core config.

    Parameters
    ----------
    endpoint : str
        The endpoint of DHub Core.
    user : str
        The user of DHub Core.
    password : str
        The password of DHub Core.
    token : str
        The token of DHub Core.

    Returns
    -------
    None
    """
    os.environ["DHUB_CORE_ENDPOINT"] = endpoint
    os.environ["DHUB_CORE_USER"] = user
    os.environ["DHUB_CORE_PASSWORD"] = password
    os.environ["DHUB_CORE_TOKEN"] = token
