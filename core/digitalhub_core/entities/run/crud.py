from __future__ import annotations

import typing

from digitalhub_core.context.builder import check_context
from digitalhub_core.entities._base.crud import delete_entity_api_ctx, list_entity_api_ctx, read_entity_api_ctx
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.entities.run.builder import run_from_dict, run_from_parameters
from digitalhub_core.utils.exceptions import EntityAlreadyExistsError, EntityError
from digitalhub_core.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.run.entity import Run


ENTITY_TYPE = EntityTypes.RUN.value


def new_run(
    project: str,
    kind: str,
    uuid: str | None = None,
    labels: list[str] | None = None,
    task: str | None = None,
    local_execution: bool = False,
    **kwargs,
) -> Run:
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
    task : str
        Name of the task associated with the run.
    local_execution : bool
        Flag to determine if object has local execution.
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    Run
        Object instance.

    Examples
    --------
    >>> obj = new_function(project="my-project",
    >>>                    name="my-function",
    >>>                    kind="python+run",
    >>>                    task="task-string"
    """
    check_context(project)
    obj = run_from_parameters(
        project=project,
        kind=kind,
        uuid=uuid,
        labels=labels,
        task=task,
        local_execution=local_execution,
        **kwargs,
    )
    obj.save()
    return obj


def get_run(
    identifier: str,
    project: str | None = None,
    **kwargs,
) -> Run:
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
    Run
        Object instance.

    Examples
    --------
    Using entity key:
    >>> obj = get_run("store://my-run-key")

    Using entity ID:
    >>> obj = get_run("my-run-id"
    >>>               project="my-project")
    """
    if not identifier.startswith("store://") and project is None:
        raise EntityError("Specify entity key or entity ID combined with project")
    obj = read_entity_api_ctx(
        identifier,
        ENTITY_TYPE,
        project=project,
        entity_id=identifier,
        **kwargs,
    )
    return run_from_dict(obj)


def list_runs(project: str, **kwargs) -> list[Run]:
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
    list[Run]
        List of object instances.

    Examples
    --------
    >>> objs = list_runs(project="my-project")
    """
    # TODO more examples: search by function, latest for task and function
    objs = list_entity_api_ctx(
        project=project,
        entity_type=ENTITY_TYPE,
        **kwargs,
    )
    return [run_from_dict(obj) for obj in objs]


def import_run(file: str) -> Run:
    """
    Get object from file.

    Parameters
    ----------
    file : str
        Path to YAML file.

    Returns
    -------
    Run
        Object instance.

    Example
    -------
    >>> obj = import_run("my-run.yaml")
    """
    dict_obj: dict = read_yaml(file)
    obj = run_from_dict(dict_obj)
    try:
        obj.save()
    except EntityAlreadyExistsError:
        pass
    finally:
        return obj


def update_run(entity: Run) -> Run:
    """
    Update object. Note that object spec are immutable.

    Parameters
    ----------
    entity : Run
        Object to update.

    Returns
    -------
    Run
        Entity updated.

    Examples
    --------
    >>> obj = update_run(obj)
    """
    return entity.save(update=True)


def delete_run(
    identifier: str,
    project: str | None = None,
    **kwargs,
) -> dict:
    """
    Delete object from backend.

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
    dict
        Response from backend.

    Examples
    --------
    >>> obj = delete_run("store://my-run-key")
    >>> obj = delete_run("my-run-id", project="my-project")
    """
    if not identifier.startswith("store://") and project is None:
        raise EntityError("Specify entity key or entity ID combined with project")
    return delete_entity_api_ctx(
        identifier=identifier,
        entity_type=ENTITY_TYPE,
        project=project,
        entity_id=identifier,
        **kwargs,
    )

    # TODO read logs
