from __future__ import annotations

from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.name import build_name
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.entities._builders.uuid import build_uuid
from digitalhub_core.entities.workflow.entity import Workflow


def workflow_from_parameters(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    **kwargs,
) -> Workflow:
    """
    Create a new object.

    Parameters
    ----------
    project : str
        Project name.
    name : str
        Object name.
    kind : str
        Kind the object.
    uuid : str
        ID of the object (UUID4, e.g. 40f25c4b-d26b-4221-b048-9527aff291e2).
    labels : list[str]
        List of labels.
    description : str
        Description of the object (human readable).
    embedded : bool
        Flag to determine if object spec must be embedded in project spec.
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    Workflow
        Object instance.
    """
    name = build_name(name)
    uuid = build_uuid(uuid)
    spec = build_spec(
        kind,
        **kwargs,
    )
    metadata = build_metadata(
        kind,
        project=project,
        name=name,
        version=uuid,
        description=description,
        labels=labels,
        embedded=embedded,
    )
    status = build_status(
        kind,
    )
    return Workflow(
        project=project,
        name=name,
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def workflow_from_dict(obj: dict) -> Workflow:
    """
    Create a new object from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    Workflow
        Object instance.
    """
    return Workflow.from_dict(obj)
