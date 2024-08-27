from __future__ import annotations

from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities._builders.uuid import build_uuid
from digitalhub_core.entities.task.entity import Task


def task_from_parameters(
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
    """
    uuid = build_uuid(uuid)
    metadata = build_metadata(
        kind=kind,
        project=project,
        name=uuid,
        labels=labels,
    )
    spec = build_spec(kind, function=function, **kwargs)
    status = build_status(kind)
    return Task(
        project=project,
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def task_from_dict(obj: dict) -> Task:
    """
    Create a new object from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary representation of Task.

    Returns
    -------
    Task
        Object instance.
    """
    return Task.from_dict(obj)
