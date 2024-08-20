from __future__ import annotations

import typing
from pathlib import Path

from digitalhub_core.context.builder import check_context
from digitalhub_core.entities._base.crud import (
    delete_entity_api_ctx,
    list_entity_api_ctx,
    read_entity_api_ctx,
    read_entity_api_ctx_versions,
)
from digitalhub_core.entities._builders.uuid import build_uuid
from digitalhub_core.entities.artifact.builder import artifact_from_dict, artifact_from_parameters
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.utils.env_utils import get_s3_bucket
from digitalhub_core.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifact.entity._base import Artifact


ENTITY_TYPE = EntityTypes.ARTIFACT.value


def create_artifact(**kwargs) -> Artifact:
    """
    Create a new artifact with the provided parameters.

    Parameters
    ----------
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    Artifact
        Object instance.
    """
    return artifact_from_parameters(**kwargs)


def create_artifact_from_dict(obj: dict) -> Artifact:
    """
    Create a new Artifact instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    Artifact
        Artifact object.
    """
    check_context(obj.get("project"))
    return artifact_from_dict(obj)


def new_artifact(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    path: str | None = None,
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
    labels : list[str]
        List of labels.
    embedded : bool
        Flag to determine if object must be embedded in project.
    path : str
        Object path on local file system or remote storage.
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    Artifact
        Object instance.
    """
    obj = create_artifact(
        project=project,
        name=name,
        kind=kind,
        uuid=uuid,
        description=description,
        labels=labels,
        embedded=embedded,
        path=path,
        **kwargs,
    )
    obj.save()
    return obj


def get_artifact(
    identifier: str,
    project: str | None = None,
    entity_id: str | None = None,
    **kwargs,
) -> Artifact:
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
    Artifact
        Object instance.
    """
    obj = read_entity_api_ctx(
        identifier,
        ENTITY_TYPE,
        project=project,
        entity_id=entity_id,
        **kwargs,
    )
    entity = artifact_from_dict(obj)
    entity._get_files_info()
    return entity


def get_artifact_versions(
    identifier: str,
    project: str | None = None,
    **kwargs,
) -> list[Artifact]:
    """
    Get object versions from backend.

    Parameters
    ----------
    identifier : str
        Entity key or name.
    project : str
        Project name.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    list[Artifact]
        List of object instances.
    """
    objs = read_entity_api_ctx_versions(
        identifier,
        entity_type=ENTITY_TYPE,
        project=project,
        **kwargs,
    )
    objects = []
    for o in objs:
        entity = artifact_from_dict(o)
        entity._get_files_info()
        objects.append(entity)
    return objects


def import_artifact(file: str) -> Artifact:
    """
    Import an Artifact object from a file using the specified file path.

    Parameters
    ----------
    file : str
        Path to the file.

    Returns
    -------
    Artifact
        Object instance.
    """
    obj: dict = read_yaml(file)
    return create_artifact_from_dict(obj)


def delete_artifact(
    identifier: str,
    project: str | None = None,
    entity_id: str | None = None,
    delete_all_versions: bool = False,
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
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    dict
        Response from backend.
    """
    return delete_entity_api_ctx(
        identifier=identifier,
        entity_type=ENTITY_TYPE,
        project=project,
        entity_id=entity_id,
        delete_all_versions=delete_all_versions,
        **kwargs,
    )


def update_artifact(entity: Artifact) -> Artifact:
    """
    Update object in backend.

    Parameters
    ----------
    entity : Artifact
        The object to update.

    Returns
    -------
    Artifact
        Entity updated.
    """
    return entity.save(update=True)


def list_artifacts(project: str, **kwargs) -> list[Artifact]:
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
    list[Artifact]
        List of artifacts.
    """
    objs = list_entity_api_ctx(
        project=project,
        entity_type=ENTITY_TYPE,
        **kwargs,
    )
    objects = []
    for o in objs:
        entity = artifact_from_dict(o)
        entity._get_files_info()
        objects.append(entity)
    return objects


def log_artifact(
    project: str,
    name: str,
    kind: str,
    source: str,
    path: str | None = None,
    **kwargs,
) -> Artifact:
    """
    Create and upload an artifact.

    Parameters
    ----------
    project : str
        Project name.
    name : str
        Object name.
    kind : str
        Kind the object.
    source : str
        Artifact location on local machine.
    path : str
        Destination path of the artifact. If not provided, it's generated.
    **kwargs : dict
        New artifact parameters.

    Returns
    -------
    Artifact
        Instance of Artifact class.
    """
    if path is None:
        uuid = build_uuid()
        kwargs["uuid"] = uuid
        path = f"s3://{get_s3_bucket()}/{project}/{ENTITY_TYPE}/{name}/{uuid}"
        if Path(source).is_dir():
            path = f"{path}/"

    obj = new_artifact(project=project, name=name, kind=kind, path=path, **kwargs)
    obj.upload(source)
    return obj
