"""
Artifact module.
"""

from sdk.client.client import Client
from sdk.entities.utils import file_importer, file_exporter, delete_from_backend
from sdk.entities.artifact.artifact import Artifact


API_CREATE = "/api/v1/artifacts"
API_READ = "/api/v1/artifacts/{}"
API_DELETE = "/api/v1/artifacts/{}"
API_READ_ALL = "/api/v1/artifacts"

OBJ_ATTR = ["project", "key", "path"]


def create_artifact(
    project: str,
    key: str,
    path: str,
) -> Artifact:
    """
    Create an Artifact instance with the given parameters.
    """
    return Artifact(project, key, path)


def get_artifact(client: Client, key: str) -> Artifact:
    """
    Retrieves artifact details from the backend.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    key : str
        The key of the artifact.

    Returns
    -------
    Artifact
        An object that contains details about the specified artifact.

    Raises
    ------
    KeyError
        If the specified artifact does not exist.

    """
    key = get_id(key, client)
    r = client.get_object(API_READ.format(key))
    if "status" not in r:
        kwargs = {
            "project": r.get("project"),
            "key": r.get("spec", {}).get("target"),
            "path": r.get("spec", {}).get("source"),
        }
        return Artifact(**kwargs)
    raise KeyError(f"Artifact {key} does not exists.")


def delete_artifact(client: Client, key: str) -> None:
    """
    Delete a artifact from backend.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    key : str
        The key of the artifact.

    Returns
    -------
    None
        This function does not return anything.
    """
    api = API_DELETE.format(get_id(key, client))
    delete_from_backend(client, api)


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
    return file_importer(file, Artifact, OBJ_ATTR)


def export_artifact(artifact: Artifact, file: str) -> None:
    """
    Export the specified Artifact object to a file in the specified location.

    Parameters
    ----------
    artifact : Artifact
        The Artifact object to be exported.
    file : str
        The absolute or relative path to the file in which the Artifact object
        will be exported.

    Returns
    -------
    None
    """
    file_exporter(file, artifact.to_dict())


def get_id(key, client):
    for i in client.get_object(API_READ_ALL):
        if i["spec"]["target"] == key:
            key = i["id"]
    return key
