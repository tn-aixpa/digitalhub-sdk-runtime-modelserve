"""
Module for performing operations on runs.
"""
from __future__ import annotations

import typing

from sdk.entities.run.entity import run_from_dict, run_from_parameters
from sdk.entities.utils.utils import check_local_flag, save_or_export
from sdk.utils.api import DTO_RUNS, api_base_delete, api_base_read
from sdk.utils.factories import get_context
from sdk.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from sdk.entities.run.entity import Run


def create_run(**kwargs) -> Run:
    """
    Create a new object instance.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    Run
       Object instance.
    """
    return run_from_parameters(**kwargs)


def new_run(
    project: str,
    task_id: str,
    task: str,
    kind: str = "run",
    inputs: dict = None,
    outputs: list = None,
    parameters: dict = None,
    local: bool = False,
) -> Run:
    """
    Create a new object instance.

    Parameters
    ----------
    project : str
        Name of the project.
    task_id : str
        The task id of the run.
    task : str
        The task string of the run.
    kind : str, default "run"
        The type of the Run.
    inputs : dict
        The inputs of the run.
    outputs : list
        The outputs of the run.
    parameters : dict
        The parameters of the run.
    local : bool
        Flag to determine if object has local execution.

    Returns
    -------
    Run
       Object instance.
    """
    check_local_flag(project, local)
    obj = create_run(
        project=project,
        task_id=task_id,
        task=task,
        kind=kind,
        inputs=inputs,
        outputs=outputs,
        parameters=parameters,
        local=local,
    )
    save_or_export(obj, local)
    return obj


def get_run(project: str, name: str) -> Run:
    """
    Get object from backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the run.

    Returns
    -------
    Run
        Object instance.
    """
    api = api_base_read(DTO_RUNS, name)
    obj = get_context(project).read_object(api)
    return run_from_dict(obj)


def import_run(file: str) -> Run:
    """
    Get object from file.

    Parameters
    ----------
    file : str
        Path to the file.

    Returns
    -------
    Run
        Object instance.
    """
    obj = read_yaml(file)
    return run_from_dict(obj)


def delete_run(project: str, name: str) -> None:
    """
    Delete run from the backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the run.

    Returns
    -------
    None
        This run does not return anything.
    """
    api = api_base_delete(DTO_RUNS, name)
    return get_context(project).delete_object(api)
