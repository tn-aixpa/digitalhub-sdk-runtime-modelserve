from __future__ import annotations

import typing

from digitalhub_core.context.builder import check_context
from digitalhub_core.entities._base.crud import delete_entity_api_ctx, list_entity_api_ctx, read_entity_api_ctx
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.entities.task.builder import task_from_dict, task_from_parameters
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.task.entity import Task


ENTITY_TYPE = EntityTypes.TASK.value


def new_task(
    project: str,
    kind: str,
    uuid: str | None = None,
    labels: list[str] | None = None,
    function: str | None = None,
    **kwargs,
) -> Task:
    """
    Create a new object.

    Parameters
    ----------
    project : str
        Project name.
    kind : str
        Kind the object.
    uuid : str
        ID of the object (UUID4, e.g. 40f25c4b-d26b-4221-b048-9527aff291e2).
    labels : list[str]
        List of labels.
    function : str
        Name of the executable associated with the task.
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    Task
        Object instance.

    Examples
    --------
    >>> obj = new_function(project="my-project",
    >>>                    name="my-function",
    >>>                    kind="python+task",
    >>>                    task="task-string"
    """
    check_context(project)
    obj = task_from_parameters(
        project=project,
        kind=kind,
        uuid=uuid,
        labels=labels,
        function=function,
        **kwargs,
    )
    obj.save()
    return obj


def get_task(
    identifier: str,
    project: str | None = None,
    **kwargs,
) -> Task:
    """
    Get object from backend.

    Parameters
    ----------
    identifier : str
        Entity key (store://...) or entity ID.
    project : str
        Project name.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    Task
        Object instance.

    Examples
    --------
    Using entity key:
    >>> obj = get_task("store://my-task-key")

    Using entity ID:
    >>> obj = get_task("my-task-id"
    >>>               project="my-project")
    """
    if not identifier.startswith("store://"):
        raise EntityError("Task has no name. Use key instead.")
    obj = read_entity_api_ctx(
        identifier,
        ENTITY_TYPE,
        project=project,
        entity_id=identifier,
        **kwargs,
    )
    return task_from_dict(obj)


def list_tasks(project: str, **kwargs) -> list[Task]:
    """
    List all latest version objects from backend.

    Parameters
    ----------
    project : str
        Project name.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    list[Task]
        List of object instances.

    Examples
    --------
    >>> objs = list_tasks(project="my-project")
    """
    objs = list_entity_api_ctx(
        project=project,
        entity_type=ENTITY_TYPE,
        **kwargs,
    )
    return [task_from_dict(obj) for obj in objs]


def import_task(file: str) -> Task:
    """
    Get object from file.

    Parameters
    ----------
    file : str
        Path to YAML file.

    Returns
    -------
    Task
        Object instance.

    Example
    -------
    >>> obj = import_task("my-task.yaml")
    """
    obj: dict = read_yaml(file)
    return task_from_dict(obj)


def update_task(entity: Task) -> Task:
    """
    Update object. Note that object spec are immutable.

    Parameters
    ----------
    entity : Task
        Object to update.

    Returns
    -------
    Task
        Entity updated.

    Examples
    --------
    >>> obj = update_task(obj)
    """
    return entity.save(update=True)


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
        Entity key (store://...) or entity name.
    project : str
        Project name.
    entity_id : str
        Entity ID.
    delete_all_versions : bool
        Delete all versions of the named entity. If True, use entity name instead of entity key as identifier.
    cascade : bool
        Cascade delete.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    dict
        Response from backend.

    Examples
    --------
    If delete_all_versions is False:
    >>> obj = delete_task("store://my-task-key")

    Otherwise:
    >>> obj = delete_task("task-name",
    >>>                  project="my-project",
    >>>                  delete_all_versions=True)
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
