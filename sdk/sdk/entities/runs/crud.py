"""
Module for performing operations on runs.
"""
from __future__ import annotations

import typing

from sdk.context.builder import get_context
from sdk.entities.runs.entity import run_from_dict, run_from_parameters
from sdk.utils.api import api_base_delete, api_base_read, api_base_update
from sdk.utils.commons import RUNS
from sdk.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from sdk.entities.runs.entity import Run


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
    task: str,
    task_id: str,
    kind: str | None = None,
    inputs: dict | None = None,
    outputs: list | None = None,
    parameters: dict | None = None,
    local_execution: bool = False,
    **kwargs,
) -> Run:
    """
    Create a new object instance.

    Parameters
    ----------
    project : str
        Name of the project.
    task : str
        The task string of the run.
    task_id : str
        The task id of the run.
    kind : str, default "run"
        The type of the Run.
    inputs : dict
        The inputs of the run.
    outputs : list
        The outputs of the run.
    parameters : dict
        The parameters of the run.
    local_execution : bool
        Flag to determine if object has local execution.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Run
       Object instance.
    """
    obj = create_run(
        project=project,
        task=task,
        task_id=task_id,
        kind=kind,
        inputs=inputs,
        outputs=outputs,
        parameters=parameters,
        local_execution=local_execution,
        **kwargs,
    )
    obj.save()
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
    api = api_base_read(RUNS, name)
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


def delete_run(project: str, name: str) -> dict:
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
    dict
        Response from backend.
    """
    api = api_base_delete(RUNS, name)
    return get_context(project).delete_object(api)


def update_run(run: Run) -> dict:
    """
    Update run in the backend. Warning, this will overwrite the entire run.
    Thi should only be used for updating the status of a run in the wrappers.

    Parameters
    ----------
    run : Run
        The run object to update.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_base_update(RUNS, run.id)
    return get_context(run.project).update_object(
        run.to_dict(include_all_non_private=True), api
    )
