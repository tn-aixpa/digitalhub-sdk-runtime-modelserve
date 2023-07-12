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


def create_run(
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
    Create a new Run instance with the given parameters.

    Parameters
    ----------
    project : str
        Name of the project.
    task_id : str
        The task id of the run.
    task : str
        The task string of the run.
    kind : str, optional, default "run"
        The type of the Run.
    inputs : dict, optional
        The inputs of the run.
    outputs : list, optional
        The outputs of the run.
    parameters : dict, optional
        The parameters of the run.
    local : bool, optional
        Flag to determine if object has local execution.
    embedded : bool, optional
        Flag to determine if object must be embedded in project.

    Returns
    -------
    Run
        Instance of the Run class representing the specified run.

    """
    return run_from_parameters(
        project=project,
        task_id=task_id,
        task=task,
        kind=kind,
        inputs=inputs,
        outputs=outputs,
        parameters=parameters,
        local=local,
    )


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
    Create a new Run instance with the given parameters.

    Parameters
    ----------
    project : str
        Name of the project.
    task_id : str
        The task id of the run.
    task : str
        The task string of the run.
    kind : str, optional, default "run"
        The type of the Run.
    inputs : dict, optional
        The inputs of the run.
    outputs : list, optional
        The outputs of the run.
    parameters : dict, optional
        The parameters of the run.
    local : bool, optional
        Flag to determine if object has local execution.

    Returns
    -------
    Run
        Instance of the Run class representing the specified run.

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
    Retrieve run details from the backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the run.

    Returns
    -------
    Run
        An object that contains details about the specified run.

    """
    api = api_base_read(DTO_RUNS, name)
    obj = get_context(project).read_object(api)
    return run_from_dict(obj)


def import_run(file: str) -> Run:
    """
    Import a Run object from a file using the specified file path.

    Parameters
    ----------
    file : str
        The absolute or relative path to the file containing the Run object.

    Returns
    -------
    Run
        The Run object imported from the file using the specified path.
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
