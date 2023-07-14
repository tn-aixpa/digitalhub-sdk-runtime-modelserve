"""
Artifact operations module.
"""
from __future__ import annotations

import typing

from sdk.entities.artifact.entity import artifact_from_dict, artifact_from_parameters
from sdk.entities.utils.utils import check_local_flag, save_or_export
from sdk.utils.api import DTO_ARTF, api_ctx_delete, api_ctx_read
from sdk.utils.factories import get_context
from sdk.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from sdk.entities.artifact.entity import Artifact


def create_artifact(**kwargs) -> Artifact:
    """
    Create a new artifact with the provided parameters.

    Parameters
    ----------
    **kwargs
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
        Dictionary to create the Artifact from.

    Returns
    -------
    Artifact
        Artifact object.
    """
    return artifact_from_dict(obj)


def new_artifact(
    project: str,
    name: str,
    description: str = "",
    kind: str = "artifact",
    key: str | None = None,
    src_path: str | None = None,
    target_path: str | None = None,
    local: bool = False,
    embedded: bool = False,
    uuid: str | None = None,
) -> Artifact:
    """
    Create an instance of the Artifact class with the provided parameters.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        Identifier of the artifact.
    description : str
        Description of the artifact.
    kind : str
        The type of the artifact.
    key : str
        Representation of artfact like store://etc..
    src_path : str
        Path to the artifact on local file system or remote storage.
    targeth_path : str
        Destination path of the artifact.
    local : bool
        Flag to determine if object has local execution.
    embedded : bool
        Flag to determine if object must be embedded in project.
    uuid : str
        UUID.

    Returns
    -------
    Artifact
       Object instance.
    """
    check_local_flag(project, local)
    obj = create_artifact(
        project=project,
        name=name,
        description=description,
        kind=kind,
        key=key,
        src_path=src_path,
        target_path=target_path,
        local=local,
        embedded=embedded,
        uuid=uuid,
    )
    save_or_export(obj, local)
    return obj


def get_artifact(project: str, name: str, uuid: str | None = None) -> Artifact:
    """
    Retrieves artifact details from the backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the artifact.
    uuid : str
        UUID.

    Returns
    -------
    Artifact
        Object instance.
    """
    api = api_ctx_read(project, DTO_ARTF, name, uuid=uuid)
    obj = get_context(project).read_object(api)
    return artifact_from_dict(obj)


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
    obj = read_yaml(file)
    return artifact_from_dict(obj)


def delete_artifact(project: str, name: str, uuid: str | None = None) -> dict:
    """
    Delete artifact from the backend. If the uuid is not specified, delete all versions.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the artifact.
    uuid : str
        UUID.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_ctx_delete(project, DTO_ARTF, name, uuid=uuid)
    return get_context(project).delete_object(api)
