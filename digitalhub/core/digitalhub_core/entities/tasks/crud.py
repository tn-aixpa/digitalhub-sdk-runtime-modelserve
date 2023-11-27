"""
Module for performing operations on tasks.
"""
from __future__ import annotations

import typing

from digitalhub_core.context.builder import get_context
from digitalhub_core.entities.tasks.entity import task_from_dict, task_from_parameters
from digitalhub_core.utils.api import api_base_delete, api_base_read, api_base_update
from digitalhub_core.utils.commons import TASK
from digitalhub_core.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.tasks.entity import Task


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
    kind: str,
    uuid: str | None = None,
    function: str | None = "",
    **kwargs,
) -> Task:
    """
    Create a new object instance.

    Parameters
    ----------
    project : str
        Name of the project.
    kind : str
        The type of the task.
    uuid : str
        UUID.
    function : str
        The function string identifying the function.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Task
       Object instance.
    """
    obj = create_task(
        project=project,
        kind=kind,
        uuid=uuid,
        function=function,
        **kwargs,
    )
    obj.save()
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
    api = api_base_read(TASK, name)
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

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_base_delete(TASK, name)
    return get_context(project).delete_object(api)


def update_task(task: Task) -> dict:
    """
    Update task.

    Parameters
    ----------
    task : Task
        The task object to update.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_base_update(TASK, task.id)
    return get_context(task.metadata.project).update_object(task.to_dict(), api)
