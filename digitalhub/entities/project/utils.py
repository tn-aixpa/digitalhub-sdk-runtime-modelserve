from __future__ import annotations

import importlib.util as imputil
import typing
from pathlib import Path
from typing import Callable

if typing.TYPE_CHECKING:
    from digitalhub.entities.project._base.entity import Project


def setup_project(project: Project, setup_kwargs: dict | None = None) -> Project:
    """
    Search for setup_project.py file and launch setup hanlder as project hook.

    Parameters
    ----------
    project : Project
        The project to scafold.
    setup_kwargs : dict
        Arguments to pass to setup handler.

    Returns
    -------
    Project
        Set up project.
    """
    setup_kwargs = setup_kwargs if setup_kwargs is not None else {}
    check_pth = Path(project.spec.context, ".CHECK")
    setup_pth = Path(project.spec.context, "setup_project.py")
    if setup_pth.exists() and not check_pth.exists():
        setup_fnc = _get_setup_function(setup_pth)
        project = setup_fnc(project, **setup_kwargs)
        check_pth.touch()
    return project


def _get_setup_function(setup_pth: Path) -> Callable:
    """
    Get setup function.

    Parameters
    ----------
    setup_pth : Path
        Path to setup file.

    Returns
    -------
    Callable
        Setup function.
    """
    spec = imputil.spec_from_file_location("setup_project", setup_pth)
    mod = imputil.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "setup")
