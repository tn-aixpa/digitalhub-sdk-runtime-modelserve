"""
Module for performing operations on tasks.
"""
from __future__ import annotations

import typing

from sdk.entities.task.entity import task_from_dict, task_from_parameters
from sdk.entities.utils.utils import check_local_flag, save_or_export
from sdk.utils.api import DTO_TASK, api_base_delete, api_base_read
from sdk.utils.factories import get_context
from sdk.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from sdk.entities.task.entity import Task


def create_task(**kwargs) -> Task:
    """
    Create a new object instance.

    Parameters
    ----------
    **kwargs
        Keyword arguments.

    Returns
    -------
    Task
       Object instance.
    """
    return task_from_parameters(**kwargs)


def new_task(
    project: str,
    kind: str = "task",
    task: str = "",
    resources: dict | None = None,
    local: bool = False,
    uuid: str | None = None,
) -> Task:
    """
    Create a new object instance.

    Parameters
    ----------
    project : str
        Name of the project.
    kind : str, default "task"
        The type of the Task.
    task : str
        The task string identifying the Task.
    resources : dict
        The Kubernetes resources for the Task.
    local : bool
        Flag to determine if object has local execution.
    uuid : str
        UUID.

    Returns
    -------
    Task
       Object instance.
    """
    check_local_flag(project, local)
    obj = create_task(
        project=project,
        kind=kind,
        task=task,
        resources=resources,
        local=local,
        uuid=uuid,
    )
    save_or_export(obj, local)
    return obj


def get_task(project: str, name: str) -> Task:
    """
    Get object from backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the task.

    Returns
    -------
    Task
        Object instance.
    """
    api = api_base_read(DTO_TASK, name)
    obj = get_context(project).read_object(api)
    return task_from_dict(obj)


def import_task(file: str) -> Task:
    """
    Get object from file.

    Parameters
    ----------
    file : str
        Path to the file.

    Returns
    -------
    Task
        Object instance.
    """
    obj = read_yaml(file)
    return task_from_dict(obj)


def delete_task(project: str, name: str) -> dict:
    """
    Delete task from the backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the task.
    uuid : str
        UUID.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_base_delete(DTO_TASK, name)
    return get_context(project).delete_object(api)
