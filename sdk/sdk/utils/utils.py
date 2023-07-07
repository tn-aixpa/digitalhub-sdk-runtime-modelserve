"""
General utilities module.
"""
import base64
from uuid import uuid4

from sdk.utils.io_utils import read_text


def get_uiid() -> str:
    """
    Create a uuid.

    Returns
    -------
    str
        The uuid.
    """
    return uuid4().hex


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
    data = read_text(path)
    return base64.b64encode(data.encode()).decode()
