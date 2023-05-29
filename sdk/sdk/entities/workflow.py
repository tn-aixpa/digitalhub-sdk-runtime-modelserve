"""
Workflow module.
"""

from sdk.client.client import Client
from sdk.utils.utils import get_uiid
from sdk.entities.utils import file_importer, file_exporter, delete_from_backend


API_CREATE = "/api/v1/workflows"
API_READ = "/api/v1/workflows/{}"
API_DELETE = "/api/v1/workflows/{}"
API_READ_ALL = "/api/v1/workflows"

OBJ_ATTR = [
    "project",
    "name",
    "kind",
]


class Workflow:
    """
    A class representing a workflow.
    """

    def __init__(
        self, project: str, name: str = None, kind: str = None, spec: dict = None
    ) -> None:
        """Initialize the Workflow instance."""
        self.project = project
        self.name = name
        self.kind = kind
        self.spec = spec if spec is not None else {}
        self.id = get_uiid()

    def save(self, client: Client, overwrite: bool = False) -> dict:
        """
        Save workflow into backend.

        Returns
        -------
        dict
            Mapping representaion of Workflow from backend.

        """
        try:
            dict_ = {
                "name": self.name,
                "project": self.project,
                "kind": self.kind,
                "spec": self.spec,
            }
            return client.create_object(dict_, API_CREATE)
        except KeyError:
            raise Exception("Workflow already present in the backend.")

    def run(self) -> "Run": ...

    def schedule(self) -> "Run": ...

    def to_dict(self) -> dict:
        """
        Return object to dict.

        Returns
        -------
        dict
            A dictionary containing the attributes of the Workflow instance.

        """
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def __repr__(self) -> str:
        """
        Return string representation of the workflow object.

        Returns
        -------
        str
            A string representing the Workflow instance.

        """
        return str(self.to_dict())


def create_workflow(
    project: str,
    name: str = None,
    kind: str = None,
    spec: dict = None,
) -> Workflow:
    """
    Create a Workflow instance with the given parameters.
    """
    return Workflow(project, name, kind, spec)


def get_workflow(client: Client, name: str) -> Workflow:
    """
    Retrieves workflow details from the backend.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    name : str
        The name of the workflow.

    Returns
    -------
    Workflow
        An object that contains details about the specified workflow.

    Raises
    ------
    KeyError
        If the specified workflow does not exist.

    """
    key = get_id(name, client)
    r = client.get_object(API_READ.format(key))
    if "status" not in r:
        kwargs = {
            "project": r.get("project"),
            "kind": r.get("kind"),
            "name": r.get("name"),
            "spec": r.get("spec"),
        }
        return Workflow(**kwargs)
    raise KeyError(f"Workflow {key} does not exists.")


def delete_workflow(client: Client, name: str) -> None:
    """
    Delete a workflow.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    name : str
        The name of the workflow.

    Returns
    -------
    None
        This function does not return anything.
    """
    api = API_DELETE.format(get_id(name, client))
    delete_from_backend(client, api)


def import_workflow(file: str) -> Workflow:
    return file_importer(file, Workflow, OBJ_ATTR)


def export_workflow(workflow: Workflow, file: str) -> None:
    file_exporter(file, workflow.to_dict())


def get_id(key, client):
    for i in client.get_object(API_READ_ALL):
        if i["name"] == key:
            key = i["id"]
    return key
