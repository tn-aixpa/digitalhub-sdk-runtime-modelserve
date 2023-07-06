"""
Common filesystem utils.
"""
import os
import shutil
from pathlib import Path


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
    if pth.suffix != "":
        return str(pth.parent)
    return str(pth)


def check_dir(path: str) -> bool:
    """
    Check if a directory exists.

    Parameters
    ----------
    path : str
        The directory path.

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
    Make a directory.

    Parameters
    ----------
    *args
        The directory path.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If the directory cannot be created.
    """
    try:
        os.makedirs(get_absolute_path(*args))
    except Exception as ex:
        raise ex


def check_make_dir(path: str) -> None:
    """
    Check if a directory already exist, otherwise create it.

    Parameters
    ----------
    path : str
        The directory path.

    Returns
    -------
    None
    """
    if not check_dir(path):
        make_dir(path)


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
# Paths utils
####################


def get_path(*args) -> str:
    """
    Return path.

    Parameters
    ----------
    *args
        Arguments to join in a path.

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
        Arguments to join in an absolute path.

    Returns
    -------
    str
        The absolute path.

    Raises
    ------
    Exception
        If the path cannot be resolved.
    """
    try:
        return str(Path(*args).absolute())
    except Exception as ex:
        raise ex


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


def copy_file(src: str, dst: str) -> None:
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
    None
    """
    shutil.copy(src, dst)


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
    if check_file(src):
        return Path(src).suffix == ".py"
