from __future__ import annotations

import typing

from oltreai_core.context.builder import check_context
from oltreai_core.entities._base.crud import (
    delete_entity_api_ctx,
    list_entity_api_ctx,
    read_entity_api_ctx,
    update_entity_api_ctx,
)
from oltreai_core.entities.entity_types import EntityTypes
from oltreai_core.entities.task.builder import task_from_dict, task_from_parameters
from oltreai_core.utils.exceptions import EntityError
from oltreai_core.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from oltreai_core.entities.task.entity import Task


ENTITY_TYPE = EntityTypes.TASK.value


def create_task(**kwargs) -> Task:
    """
    Create a new object instance.

    Parameters
    ----------
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    Task
        Object instance.
    """
    return task_from_parameters(**kwargs)


def create_task_from_dict(obj: dict) -> Task:
    """
    Create a new object instance.

    Parameters
    ----------
    obj : dict
        Object dictionary.

    Returns
    -------
    Task
        Object instance.
    """
    check_context(obj.get("project"))
    return task_from_dict(obj)


def new_task(
    project: str,
    task: str,
    kind: str,
    uuid: str | None = None,
    git_source: str | None = None,
    labels: list[str] | None = None,
    **kwargs,
) -> Task:
    """
    Create a new object instance.

    Parameters
    ----------
    project : str
        Project name.
    task : str
        The task string identifying the task.
    kind : str
        Kind the object.
    uuid : str
        ID of the object (UUID4).
    git_source : str
        Remote git source for object.
    labels : list[str]
        List of labels.
    task : str
        The task string identifying the task.
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    Task
        Object instance.
    """
    obj = create_task(
        project=project,
        task=task,
        kind=kind,
        uuid=uuid,
        git_source=git_source,
        labels=labels,
        **kwargs,
    )
    obj.save()
    return obj


def get_task(
    identifier: str,
    project: str | None = None,
    entity_id: str | None = None,
    **kwargs,
) -> Task:
    """
    Get object from backend.

    Parameters
    ----------
    identifier : str
        Entity key or name.
    project : str
        Project name.
    entity_id : str
        Entity ID.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    Task
        Object instance.
    """
    if not identifier.startswith("store://"):
        raise EntityError("Task has no name. Use key instead.")
    obj = read_entity_api_ctx(
        identifier,
        ENTITY_TYPE,
        project=project,
        entity_id=entity_id,
        **kwargs,
    )
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
    obj: dict = read_yaml(file)
    return create_task_from_dict(obj)


def delete_task(
    identifier: str,
    project: str | None = None,
    entity_id: str | None = None,
    delete_all_versions: bool = False,
    cascade: bool = True,
    **kwargs,
) -> dict:
    """
    Delete object from backend.

    Parameters
    ----------
    identifier : str
        Entity key or name.
    project : str
        Project name.
    entity_id : str
        Entity ID.
    delete_all_versions : bool
        Delete all versions of the named entity.
        Use entity name instead of entity key as identifier.
    cascade : bool
        Cascade delete.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    dict
        Response from backend.
    """
    if not identifier.startswith("store://"):
        raise EntityError("Task has no name. Use key instead.")
    return delete_entity_api_ctx(
        identifier=identifier,
        entity_type=ENTITY_TYPE,
        project=project,
        entity_id=entity_id,
        delete_all_versions=delete_all_versions,
        cascade=cascade,
        **kwargs,
    )


def update_task(entity: Task) -> Task:
    """
    Update object in backend.

    Parameters
    ----------
    entity : Task
        The object to update.

    Returns
    -------
    Task
        Entity updated.
    """
    return entity.save(update=True)


def list_tasks(project: str, **kwargs) -> list[Task]:
    """
    List all objects from backend.

    Parameters
    ----------
    project : str
        Project name.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    list[Task]
        List of tasks.
    """
    objs = list_entity_api_ctx(
        project=project,
        entity_type=ENTITY_TYPE,
        **kwargs,
    )
    return [task_from_dict(obj) for obj in objs]
