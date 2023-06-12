"""
Common URI utils.
"""
from pathlib import Path
from urllib.parse import ParseResult, urljoin, urlparse, urlunparse


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
    Return URI netloc.

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


def build_key(dst: str, *args) -> str:
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
    key = str(Path(get_uri_path(dst), *args))
    if key.startswith("/"):
        key = key[1:]
    return key


def rebuild_uri(uri: str, *args) -> str:
    """
    Rebuild an URI.

    Parameters
    ----------
    uri : str
        URI.

    Returns
    -------
    str
        Rebuilt URI.
    """
    parsed = parse_uri(uri)
    new_path = str(Path(parsed.path, *args))
    new_uri = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            new_path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )
    return new_uri


def check_url(url: str) -> str:
    """
    Parse an URL and clean it from double '/' character.

    Parameters
    ----------
    url : str
        URL.

    Returns
    -------
    str
        Cleaned URL.
    """
    parsed = get_uri_path(url).replace("//", "/")
    return urljoin(url, parsed)


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
    If path is a relative path, it will be returned as is.
    """
    try:
        return Path(path).as_uri()
    except ValueError as ve:
        if "relative path can't be expressed as a file URI" in ve.args[0]:
            return path
