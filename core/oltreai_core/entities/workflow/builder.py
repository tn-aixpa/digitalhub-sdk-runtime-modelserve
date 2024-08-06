from __future__ import annotations

from oltreai_core.entities._builders.metadata import build_metadata
from oltreai_core.entities._builders.name import build_name
from oltreai_core.entities._builders.spec import build_spec
from oltreai_core.entities._builders.status import build_status
from oltreai_core.entities._builders.uuid import build_uuid
from oltreai_core.entities.workflow.entity import Workflow


def workflow_from_parameters(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    git_source: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    **kwargs,
) -> Workflow:
    """
    Create a new Workflow instance with the specified parameters.

    Parameters
    ----------
    project : str
        Project name.
    name : str
        Object name.
    kind : str
        Kind the object.
    uuid : str
        ID of the object (UUID4).
    git_source : str
        Remote git source for object.
    labels : list[str]
        List of labels.
    description : str
        Description of the object (human readable).
    embedded : bool
        Flag to determine if object must be embedded in project.
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    Workflow
        An instance of the created workflow.
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
        source=git_source,
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
    Create Workflow instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    Workflow
        Workflow instance.
    """
    return Workflow.from_dict(obj)
