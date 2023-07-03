"""
Artifact operations module.
"""
from sdk.entities.artifact.entity import Artifact, ArtifactMetadata, ArtifactSpec
from sdk.utils.api import DTO_ARTF, delete_api, read_api
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context
from sdk.utils.io_utils import read_yaml


def new_artifact(
    project: str,
    name: str,
    description: str = None,
    kind: str = None,
    key: str = None,
    src_path: str = None,
    target_path: str = None,
    local: bool = False,
    embed: bool = False,
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
    embed : bool, optional
        Flag to determine if object must be embedded in project.

    Returns
    -------
    Artifact
        Instance of the Artifact class representing the specified artifact.
    """
    context = get_context(project)
    if context.local != local:
        raise EntityError("Context local flag does not match local flag of artifact")
    meta = ArtifactMetadata(name=name, description=description)
    spec = ArtifactSpec(key=key, src_path=src_path, target_path=target_path)
    obj = Artifact(
        project=project,
        name=name,
        kind=kind,
        metadata=meta,
        spec=spec,
        local=local,
        embed=embed,
    )
    if local:
        obj.export()
    else:
        obj.save()
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

    Raises
    ------
    KeyError
        If the specified artifact does not exist.

    """
    context = get_context(project)
    api = read_api(project, DTO_ARTF, name, uuid=uuid)
    obj = context.client.get_object(api)
    return Artifact.from_dict(obj)


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
    return Artifact.from_dict(obj)


def delete_artifact(project: str, name: str, uuid: str = None) -> None:
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
    None
        This function does not return anything.
    """
    context = get_context(project)
    api = delete_api(project, DTO_ARTF, name, uuid=uuid)
    obj = context.client.delete_object(api)
    return obj
