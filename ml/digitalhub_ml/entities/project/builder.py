from __future__ import annotations

from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.name import build_name
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_ml.entities.project.entity import ProjectMl


def project_from_parameters(
    name: str,
    kind: str,
    description: str | None = None,
    labels: list[str] | None = None,
    local: bool = False,
    context: str | None = None,
    **kwargs,
) -> ProjectMl:
    """
    Create project.

    Parameters
    ----------
    name : str
        Object name.
    kind : str
        Kind the object.
    description : str
        Description of the object (human readable).
    labels : list[str]
        List of labels.
    local : bool
        Flag to determine if object will be exported to backend.
    context : str
        The context of the project.
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    ProjectMl
        ProjectMl object.
    """
    name = build_name(name)
    spec = build_spec(
        kind,
        context=context,
        **kwargs,
    )
    metadata = build_metadata(
        kind,
        project=name,
        name=name,
        description=description,
        labels=labels,
    )
    status = build_status(kind)
    return ProjectMl(
        name=name,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
        local=local,
    )


def project_from_dict(obj: dict) -> ProjectMl:
    """
    Create project from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    ProjectMl
        ProjectMl object.
    """
    return ProjectMl.from_dict(obj)
