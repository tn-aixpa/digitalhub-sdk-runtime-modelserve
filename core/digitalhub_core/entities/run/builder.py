from __future__ import annotations

from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities._builders.uuid import build_uuid
from digitalhub_core.entities.run.entity import Run


def run_from_parameters(
    project: str,
    kind: str,
    uuid: str | None = None,
    labels: list[str] | None = None,
    task: str | None = None,
    local_execution: bool = False,
    **kwargs,
) -> Run:
    """
    Create run.

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
    """
    uuid = build_uuid(uuid)
    metadata = build_metadata(
        kind=kind,
        project=project,
        name=uuid,
        labels=labels,
    )
    spec = build_spec(kind, task=task, local_execution=local_execution, **kwargs)
    status = build_status(kind)
    return Run(
        project=project,
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def run_from_dict(obj: dict) -> Run:
    """
    Create a new object from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    Run
        Object instance.
    """
    return Run.from_dict(obj)
