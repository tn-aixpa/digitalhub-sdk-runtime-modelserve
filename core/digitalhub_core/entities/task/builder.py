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
    **kwargs,
) -> Task:
    """
    Create a new object instance.

    Parameters
    ----------
    project : str
        Project name.
    kind : str
        Kind the object.
    uuid : str
        ID of the object (UUID4).
    labels : list[str]
        List of labels.
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
    spec = build_spec(kind, **kwargs)
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
    Create Task object from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary representation of Task.

    Returns
    -------
    Task
        Task object.
    """
    return Task.from_dict(obj)
