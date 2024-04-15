from __future__ import annotations

import os
import shutil
from pathlib import Path
from urllib.parse import urlparse

from git import Repo


def clone_repository(url: str, path: Path) -> None:
    """
    Clone git repository.

    Parameters
    ----------
    url : str
        URL of the repository.
    path : Path
        Path where to save the repository.

    Returns
    -------
    None
    """
    clean_path(path)
    url = url.replace("git+", "")
    url = add_credentials_git_remote_url(url)
    clone_from_url(url, path)


def clean_path(path: Path) -> None:
    """
    Clean path.

    Parameters
    ----------
    path : Path

    Returns
    -------
    None
    """

    shutil.rmtree(path, ignore_errors=True)


def get_git_username_password_from_token(token: str) -> tuple[str, str]:
    """
    Parse token to get username and password.

    Parameters
    ----------
    token : str
        Token to parse.

    Returns
    -------
    tuple[str, str]
        Username and password.
    """
    # Mutued from mlrun
    if token.startswith("github_pat_") or token.startswith("glpat"):
        username = "oauth2"
        password = token
    else:
        username = token
        password = "x-oauth-basic"
    return username, password


def add_credentials_git_remote_url(url: str) -> str:
    """
    Add credentials to git remote url.

    Parameters
    ----------
    url : str
        URL of the repository.

    Returns
    -------
    str
        URL with credentials.
    """
    url_obj = urlparse(url)

    # Get credentials from environment variables
    username = os.getenv("GIT_USERNAME")
    password = os.getenv("GIT_PASSWORD")
    token = os.getenv("GIT_TOKEN")

    # Get credentials from token
    if token is not None:
        username, password = get_git_username_password_from_token(token)

    if username is not None and password is not None:
        return f"https://{username}:{password}@{url_obj.hostname}{url_obj.path}"

    return url


def clone_from_url(path: Path, source: str) -> None:
    """
    Clone repository from url. Wraps git.Repo.clone_from.

    Parameters
    ----------
    path : Path
        Path where to save the repository.
    source : str
        HTTP(S) URL of the repository.

    Returns
    -------
    None
    """
    Repo.clone_from(url=source, to_path=path)
