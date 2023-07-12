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


def create_task(
    project: str,
    kind: str = "task",
    task: str = "",
    k8s_resources: dict = None,
    local: bool = False,
    uuid: str = None,
) -> Task:
    """
    Create a new Task instance with the given parameters.

    Parameters
    ----------
    project : str
        Name of the project.
    kind : str, optional, default "task"
        The type of the Task.
    task : str, optional
        The task string identifying the Task.
    k8s_resources : dict, optional
        The Kubernetes resources for the Task.
    local : bool, optional
        Flag to determine if object has local execution.
    uuid : str, optional
        UUID.

    Returns
    -------
    Task
        Instance of the Task class representing the specified task.

    """
    return task_from_parameters(
        project=project,
        kind=kind,
        task=task,
        k8s_resources=k8s_resources,
        local=local,
        uuid=uuid,
    )


def new_task(
    project: str,
    kind: str = "task",
    task: str = "",
    k8s_resources: dict = None,
    local: bool = False,
    uuid: str = None,
) -> Task:
    """
    Create a new Task instance with the given parameters.

    Parameters
    ----------
    project : str
        Name of the project.
    kind : str, optional, default "task"
        The type of the Task.
    task : str, optional
        The task string identifying the Task.
    k8s_resources : dict, optional
        The Kubernetes resources for the Task.
    local : bool, optional
        Flag to determine if object has local execution.
    uuid : str, optional
        UUID.

    Returns
    -------
    Task
        Instance of the Task class representing the specified task.

    """
    check_local_flag(project, local)
    obj = create_task(
        project=project,
        kind=kind,
        task=task,
        k8s_resources=k8s_resources,
        local=local,
        uuid=uuid,
    )
    save_or_export(obj, local)
    return obj


def get_task(project: str, name: str) -> Task:
    """
    Retrieve task details from the backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the task.

    Returns
    -------
    Task
        An object that contains details about the specified task.

    """
    api = api_base_read(DTO_TASK, name)
    obj = get_context(project).read_object(api)
    return task_from_dict(obj)


def import_task(file: str) -> Task:
    """
    Import a Task object from a file using the specified file path.

    Parameters
    ----------
    file : str
        The absolute or relative path to the file containing the Task object.

    Returns
    -------
    Task
        The Task object imported from the file using the specified path.
    """
    obj = read_yaml(file)
    return task_from_dict(obj)


def delete_task(project: str, name: str) -> None:
    """
    Delete task from the backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the task.
    uuid : str, optional
        UUID of task specific version.

    Returns
    -------
    None
        This task does not return anything.
    """
    api = api_base_delete(DTO_TASK, name)
    return get_context(project).delete_object(api)
