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


def create_artifact(
    project: str,
    name: str,
    description: str = "",
    kind: str = "artifact",
    key: str = None,
    src_path: str = None,
    target_path: str = None,
    local: bool = False,
    embedded: bool = False,
    uuid: str = None,
) -> Artifact:
    """
    Create a new artifact with the provided parameters.

    Parameters
    ----------
    project : str
        Name of the project associated with the artifact.
    name : str
        Identifier of the artifact.
    description : str, optional
        Description of the artifact.
    kind : str, optional
        The type of the artifact.
    key : str
        Representation of artfact like store://etc..
    src_path : str
        Path to the artifact on local file system or remote storage.
    targeth_path : str
        Destination path of the artifact.
    local : bool, optional
        Flag to determine if object has local execution.
    embedded : bool, optional
        Flag to determine if object must be embedded in project.
    uuid : str, optional
        UUID.

    Returns
    -------
    Artifact
        An instance of the Artifact class representing the specified artifact.
    """
    return artifact_from_parameters(
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
    key: str = None,
    src_path: str = None,
    target_path: str = None,
    local: bool = False,
    embedded: bool = False,
    uuid: str = None,
) -> Artifact:
    """
    Create an instance of the Artifact class with the provided parameters.

    Parameters
    ----------
    project : str
        Name of the project associated with the artifact.
    name : str
        Identifier of the artifact.
    description : str, optional
        Description of the artifact.
    kind : str, optional
        The type of the artifact.
    key : str
        Representation of artfact like store://etc..
    src_path : str
        Path to the artifact on local file system or remote storage.
    targeth_path : str
        Destination path of the artifact.
    local : bool, optional
        Flag to determine if object has local execution.
    embedded : bool, optional
        Flag to determine if object must be embedded in project.
    uuid : str, optional
        UUID.

    Returns
    -------
    Artifact
        Instance of the Artifact class representing the specified artifact.
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


def get_artifact(project: str, name: str, uuid: str = None) -> Artifact:
    """
    Retrieves artifact details from the backend.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the artifact.
    uuid : str, optional
        UUID of artifact specific version.

    Returns
    -------
    Artifact
        An object that contains details about the specified artifact.

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
        The absolute or relative path to the file containing the Artifact object.

    Returns
    -------
    Artifact
        The Artifact object imported from the file using the specified path.

    """
    obj = read_yaml(file)
    return artifact_from_dict(obj)


def delete_artifact(project: str, name: str, uuid: str = None) -> dict:
    """
    Delete artifact from the backend. If the uuid is not specified, delete all versions.

    Parameters
    ----------
    project : str
        Name of the project.
    name : str
        The name of the artifact.
    uuid : str, optional
        UUID of artifact specific version.

    Returns
    -------
    dict
        Response from backend.
    """
    api = api_ctx_delete(project, DTO_ARTF, name, uuid=uuid)
    return get_context(project).delete_object(api)
