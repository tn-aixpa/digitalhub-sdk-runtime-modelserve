"""
Artifact module.
"""

from sdk.client.client import Client
from sdk.entities.utils import file_importer, delete_from_backend
from sdk.entities.artifact.artifact import Artifact, ArtifactMetadata, ArtifactSpec
from sdk.utils.common import (
    API_READ_LATEST,
    API_READ_VERSION,
    API_DELETE_VERSION,
    API_DELETE_ALL,
    DTO_ARTF,
)


def new_artifact(
    project: str,
    name: str,
    description: str = None,
    kind: str = None,
    key: str = None,
    path: str = None,
    client: Client = None,
    local: bool = False,
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
    path : str
        Path to the artifact on local file system or remote storage.
    client : Client, optional
        A Client object to interact with backend.
    local : bool, optional
        Flag to determine if object wil be saved locally.

    Returns
    -------
    Artifact
        Instance of the Artifact class representing the specified artifact.
    """
    meta = ArtifactMetadata(name=name, description=description)
    spec = ArtifactSpec(key=key, path=path)
    obj = Artifact(project, name, kind, meta, spec)
    if not local:
        obj.save(client)
    return obj


def get_artifact(client: Client, project: str, name: str, uuid: str = None) -> Artifact:
    """
    Retrieves artifact details from the backend.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
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
    if uuid is not None:
        api = API_READ_VERSION.format(project, DTO_ARTF, name, uuid)
    else:
        api = API_READ_LATEST.format(project, DTO_ARTF, name)

    r = client.get_object(api)
    if "status" not in r:
        return Artifact(**r)
    raise KeyError(f"Artifact {name} does not exists.")


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
    return file_importer(file, Artifact,)


def delete_artifact(client: Client, project: str, name: str, uuid: str = None) -> None:
    """
    Delete a artifact from backend.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
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
    if uuid is not None:
        api = API_DELETE_VERSION.format(project, DTO_ARTF, name, uuid)
    else:
        api = API_DELETE_ALL.format(project, DTO_ARTF, name)
    return delete_from_backend(client, api)
