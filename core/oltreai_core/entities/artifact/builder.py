from __future__ import annotations

import typing

from oltreai_core.entities._builders.metadata import build_metadata
from oltreai_core.entities._builders.name import build_name
from oltreai_core.entities._builders.spec import build_spec
from oltreai_core.entities._builders.status import build_status
from oltreai_core.entities._builders.uuid import build_uuid
from oltreai_core.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from oltreai_core.entities.artifact.entity._base import Artifact

# Manage class mapper
cls_mapper = {}

try:
    from oltreai_core.entities.artifact.entity.artifact import ArtifactArtifact

    cls_mapper["artifact"] = ArtifactArtifact
except ImportError:
    pass


def _choose_artifact_type(kind: str) -> type[Artifact]:
    """
    Choose class based on kind.

    Parameters
    ----------
    kind : str
        Kind the object.

    Returns
    -------
    type[Artifact]
        Class of the artifact.
    """
    try:
        return cls_mapper[kind]
    except KeyError:
        raise EntityError(f"Unknown artifact kind: {kind}")


def artifact_from_parameters(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    git_source: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    path: str | None = None,
    src_path: str | None = None,
    **kwargs,
) -> Artifact:
    """
    Create an instance of the Artifact class with the provided parameters.

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
    description : str
        Description of the object (human readable).
    git_source : str
        Remote git source for object.
    labels : list[str]
        List of labels.
    embedded : bool
        Flag to determine if object must be embedded in project.
    path : str
        Object path on local file system or remote storage.
        If not provided, it's generated.
    src_path : str
        Local object path.
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    Artifact
        Artifact object.
    """
    if path is None:
        raise EntityError("Path must be provided.")
    name = build_name(name)
    uuid = build_uuid(uuid)
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
    spec = build_spec(
        kind,
        path=path,
        src_path=src_path,
        **kwargs,
    )
    status = build_status(kind)
    cls = _choose_artifact_type(kind)
    return cls(
        project=project,
        name=name,
        uuid=uuid,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
    )


def artifact_from_dict(obj: dict) -> Artifact:
    """
    Create artifact from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    Artifact
        Artifact object.
    """
    kind = obj.get("kind")
    cls = _choose_artifact_type(kind)
    return cls.from_dict(obj)
