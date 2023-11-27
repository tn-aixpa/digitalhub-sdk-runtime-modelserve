"""
Common filesystem utils.
"""
from __future__ import annotations

import shutil
from pathlib import Path

####################
# Paths utils
####################


def build_path(*args) -> str:
    """
    Build path from args list.

    Parameters
    ----------
    *args
        Arguments list.

    Returns
    -------
    str
        The path.
    """
    return str(Path(*args))


def get_absolute_path(*args) -> str:
    """
    Return absolute path.

    Parameters
    ----------
    *args
        Arguments list.

    Returns
    -------
    str
        The absolute path.
    """
    return str(Path(*args).absolute())


def check_path(path: str) -> bool:
    """
    Check if the path exists.

    Parameters
    ----------
    path : str
        The path to check.

    Returns
    -------
    bool
        True if the path exists, False otherwise.
    """
    try:
        return Path(path).exists()
    except OSError:
        return False


def clean_all(path: str) -> None:
    """
    Remove dir and all it's contents.

    Parameters
    ----------
    path : str
        The directory path.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If the directory cannot be removed.
    """
    shutil.rmtree(path)


####################
# Directories utils
####################


def get_dir(path: str) -> str:
    """
    Return directory path.

    Parameters
    ----------
    path : str
        The path.

    Returns
    -------
    str
        The directory path.
    """
    pth = Path(path)
    if pth.is_file():
        return str(pth.parent)
    return str(pth)


def check_dir(path: str) -> bool:
    """
    Check if path is a directory.

    Parameters
    ----------
    path : str
        The path to check.

    Returns
    -------
    bool
        True if the directory exists, False otherwise.
    """
    try:
        return Path(path).is_dir()
    except OSError:
        return False


def make_dir(*args) -> None:
    """
    Create a directory.

    Parameters
    ----------
    *args
        Arguments list.

    Returns
    -------
    None
    """
    pth = Path(*args).absolute()
    if pth.suffix != "":
        pth = pth.parent
    pth.mkdir(parents=True, exist_ok=True)


####################
# Files utils
####################


def check_file(path: str) -> bool:
    """
    Check if a path is a file.

    Parameters
    ----------
    path : str
        The file path.

    Returns
    -------
    bool
        True if the file exists, False otherwise.
    """
    try:
        return Path(path).is_file()
    except OSError:
        return False


def copy_file(src: str, dst: str) -> str:
    """
    Copy local file to destination.

    Parameters
    ----------
    src : str
        The source file.
    dst : str
        The destination file/directory.

    Returns
    -------
    str
        The copied file path.
    """
    return shutil.copy(src, dst)


def is_python_module(src: str) -> bool:
    """
    Check if a file is a python module.

    Parameters
    ----------
    src : str
        The file path.

    Returns
    -------
    bool
        True if the file is a python module, False otherwise.
    """
    return Path(src).suffix == ".py" and check_file(src)
