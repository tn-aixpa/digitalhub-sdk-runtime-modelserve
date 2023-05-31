"""
Workflow module.
"""

from sdk.client.client import Client
from sdk.entities.utils import file_importer, delete_from_backend
from sdk.entities.workflow.workflow import Workflow
from sdk.utils.common import (
    API_READ_LATEST,
    API_READ_VERSION,
    API_DELETE_VERSION,
    API_DELETE_ALL,
    DTO_WKFL,
)


OBJ_ATTR = [
    "project",
    "name",
    "kind",
]


def create_workflow(
    project: str,
    name: str,
    kind: str = None,
    spec: dict = None,
    client: Client = None,
    local: bool = False,
    filename: str = None,
) -> Workflow:
    """
    Create a new Workflow instance with the specified parameters.

    Parameters
    ----------
    project : str
        A string representing the project associated with this workflow.
    name : str
        The name of the workflow.
    kind : str, optional
        The kind of the workflow.
    spec : dict, optional
        The specification for the workflow.
    client : Client, optional
        A Client object to interact with backend.
    local : bool, optional
        Flag to determine if object wil be saved locally.
    filename : str, optional
        Filename to export object.

    Returns
    -------
    Workflow
        An instance of the created workflow.

    """
    obj = Workflow(project, name, kind, spec)
    if local:
        obj.export(filename)
    else:
        obj.save(client)
    return obj


def get_workflow(client: Client, project: str, name: str, uuid: str = None) -> Workflow:
    """
    Retrieves workflow details from the backend.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    project : str
        Name of the project.
    name : str
        The name of the workflow.
    uuid : str, optional
        UUID of workflow specific version.

    Returns
    -------
    Workflow
        An object that contains details about the specified workflow.

    Raises
    ------
    KeyError
        If the specified workflow does not exist.

    """
    if uuid is not None:
        api = API_READ_VERSION.format(project, DTO_WKFL, name, uuid)
    else:
        api = API_READ_LATEST.format(project, DTO_WKFL, name)

    r = client.get_object(api)
    if "status" not in r:
        kwargs = {
            "project": r.get("project"),
            "kind": r.get("kind"),
            "name": r.get("name"),
            "spec": r.get("spec"),
        }
        return Workflow(**kwargs)
    raise KeyError(f"Workflow {name} does not exists.")


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


def delete_workflow(client: Client, project: str, name: str, uuid: str = None) -> None:
    """
    Delete a workflow.

    Parameters
    ----------
    client : Client
        The client for DHUB backend.
    project : str
        Name of the project.
    name : str
        The name of the workflow.
    uuid : str, optional
        UUID of workflow specific version.

    Returns
    -------
    None
        This function does not return anything.
    """
    if uuid is not None:
        api = API_DELETE_VERSION.format(project, DTO_WKFL, name, uuid)
    else:
        api = API_DELETE_ALL.format(project, DTO_WKFL, name)
    return delete_from_backend(client, api)
