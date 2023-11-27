"""
Common URI utils.
"""
from __future__ import annotations

from pathlib import Path
from urllib.parse import ParseResult, urlparse


def parse_uri(uri: str) -> ParseResult:
    """
    Parse an uri.

    Parameters
    ----------
    uri : str
        URI.

    Returns
    -------
    ParseResult
        ParseResult object.
    """
    return urlparse(uri)


def get_uri_scheme(uri: str) -> str:
    """
    Get scheme of an URI.

    Parameters
    ----------
    uri : str
        URI.

    Returns
    -------
    str
        URI scheme.
    """
    return parse_uri(uri).scheme


def get_uri_netloc(uri: str) -> str:
    """
    Return URI netloc/bucket.

    Parameters
    ----------
    uri : str
        URI.

    Returns
    -------
    str
        URI netloc.
    """
    return parse_uri(uri).netloc


def get_uri_path(uri: str) -> str:
    """
    Return URI path.

    Parameters
    ----------
    uri : str
        URI.

    Returns
    -------
    str
        URI path.
    """
    return parse_uri(uri).path


def get_name_from_uri(uri: str) -> str:
    """
    Return filename from uri.

    Parameters
    ----------
    uri : str
        URI.

    Returns
    -------
    str
        Filename.
    """
    return Path(uri).name


def get_extension(uri: str) -> str:
    """
    Return extension from uri.

    Parameters
    ----------
    uri : str
        URI.

    Returns
    -------
    str
        Extension.
    """
    return Path(uri).suffix[1:]


def build_key(dst: str) -> str:
    """
    Build key to upload objects.

    Parameters
    ----------
    dst : str
        Destination URI.

    Returns
    -------
    str
        Key.
    """
    key = get_uri_path(dst)
    if key.startswith("/"):
        key = key[1:]
    return key


def as_uri(path: str) -> str:
    """
    Convert a path to an URI.

    Parameters
    ----------
    path : str
        Path.

    Returns
    -------
    str
        URI.

    Notes
    -----
    If path is a relative path, it will be returned as it is.
    """
    try:
        return Path(path).as_uri()
    except Exception as exc:
        if "relative path can't be expressed as a file URI" in exc.args[0]:
            return path
        raise exc


def map_uri_scheme(uri: str) -> str:
    """
    Map an URI scheme to a common scheme.

    Parameters
    ----------
    uri : str
        URI.

    Returns
    -------
    str
        Mapped scheme type.

    Raises
    ------
    ValueError
        If the scheme is unknown.
    """
    scheme = get_uri_scheme(uri)
    if scheme in ["", "file", "local"]:
        return "local"
    if scheme in ["http", "https", "remote"]:
        return "remote"
    if scheme in ["s3", "s3a", "s3n"]:
        return "s3"
    if scheme in ["sql", "postgresql"]:
        return "sql"
    raise ValueError(f"Unknown scheme '{scheme}'!")
