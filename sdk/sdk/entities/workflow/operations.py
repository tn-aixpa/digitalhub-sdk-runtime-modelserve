"""
Workflow module.
"""

from sdk.client.client import Client
from sdk.entities.utils import file_importer, file_exporter, delete_from_backend
from sdk.entities.workflow.workflow import Workflow


API_CREATE = "/api/v1/workflows"
API_READ = "/api/v1/workflows/{}"
API_DELETE = "/api/v1/workflows/{}"
API_READ_ALL = "/api/v1/workflows"

OBJ_ATTR = [
    "project",
    "name",
    "kind",
]


def create_workflow(
    project: str,
    name: str = None,
    kind: str = None,
    spec: dict = None,
) -> Workflow:
    """
    Create a new Workflow instance with the specified parameters.

    Parameters
    ----------
    project : str
        A string representing the project associated with this workflow.
    name : str, optional
        A string representing the name of the workflow.
    kind : str, optional
        The kind of the workflow.
    spec : dict, optional
        The specification for the workflow.

    Returns
    -------
    Workflow
        An instance of the created workflow.

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
    """
    Import an Workflow object from a file using the specified file path.

    Parameters
    ----------
    file : str
        The absolute or relative path to the file containing the Workflow object.

    Returns
    -------
    Workflow
        The Workflow object imported from the file using the specified path.

    """
    return file_importer(file, Workflow, OBJ_ATTR)


def export_workflow(workflow: Workflow, file: str) -> None:
    """
    Export the specified Workflow object to a file in the specified location.

    Parameters
    ----------
    workflow : Workflow
        The Workflow object to be exported.
    file : str
        The absolute or relative path to the file in which the Workflow object
        will be exported.

    Returns
    -------
    None
    """
    file_exporter(file, workflow.to_dict())


def get_id(key, client):
    for i in client.get_object(API_READ_ALL):
        if i["name"] == key:
            key = i["id"]
    return key
