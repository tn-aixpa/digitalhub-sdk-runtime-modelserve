"""
Artifact module.
"""

from sdk.client.client import Client
from sdk.utils.utils import write_yaml, read_yaml, get_uiid


API_CREATE = "/api/v1/artifacts"
API_READ = "/api/v1/artifacts/{}"
API_DELETE = "/api/v1/artifacts/{}"
API_READ_ALL = "/api/v1/artifacts"

OBJ_ATTR = ["project", "key", "path", "id"]


class Artifact:
    """
    A class representing a artifact.
    """

    def __init__(
        self,
        project: str,
        key: str,
        path: str,
    ) -> None:
        """Initialize the Artifact instance."""
        self.project = project
        self.key = key
        self.path = path
        self.id = get_uiid()

    def save(self, client: Client, overwrite: bool = False) -> dict:
        """
        Save artifact into backend.

        Returns
        -------
        dict
            Mapping representaion of Artifact from backend.

        """
        try:
            dict_ = {
                "name": self.id,
                "project": self.project,
                "kind": "job",
                "spec": {
                    "type": "artifact",
                    "target": self.key,
                    "source": self.path,
                },
                "type": "apache-parquet",
            }
            return client.create_object(dict_, API_CREATE)
        except KeyError:
            raise Exception("Artifact already present in the backend.")

    def to_dict(self) -> dict:
        """
        Return object to dict.

        Returns
        -------
        dict
            A dictionary containing the attributes of the Artifact instance.

        """
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def __repr__(self) -> str:
        """
        Return string representation of the artifact object.

        Returns
        -------
        str
            A string representing the Artifact instance.

        """
        return str(self.to_dict())


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
            "project": r["project"],
            "key": r["spec"]["target"],
            "path": r["spec"]["source"],
        }
        return Artifact(**kwargs)
    raise KeyError(f"Artifact {key} does not exists.")


def delete_artifact(client: Client, key: str) -> None:
    """
    Delete a artifact.

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

    Raises
    ------
    Any exceptions raised by the client object's delete_object method.
    """
    key = get_id(key, client)
    client.delete_object(API_DELETE.format(key))


def import_artifact(file: str) -> Artifact:
    dict_ = read_yaml(file)
    kwargs = {k: v for k, v in dict_.items() if k in OBJ_ATTR}
    artifact = Artifact(**kwargs)
    try:
        artifact.id = dict_["id"]
    except:
        ...
    return artifact


def export_artifact(artifact: Artifact, file: str) -> None:
    data = artifact.to_dict()
    write_yaml(data, file)


def get_id(key, client):
    for i in client.get_object(API_READ_ALL):
        if i["spec"]["target"] == key:
            key = i["id"]
    return key
