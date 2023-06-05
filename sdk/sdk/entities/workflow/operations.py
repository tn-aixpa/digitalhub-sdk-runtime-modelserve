"""
Workflow operations module.
"""
from sdk.client.factory import get_client
from sdk.entities.utils import file_importer
from sdk.entities.workflow.workflow import Workflow, WorkflowMetadata, WorkflowSpec
from sdk.entities.api import (
    API_DELETE_ALL,
    API_DELETE_VERSION,
    API_READ_LATEST,
    API_READ_VERSION,
    DTO_WKFL,
)


def new_workflow(
    project: str,
    name: str,
    description: str = None,
    kind: str = None,
    test: str = None,
    local: bool = False,
    save: bool = False,
) -> Workflow:
    """
    Create a new Workflow instance with the specified parameters.

    Parameters
    ----------
    project : str
        A string representing the project associated with this workflow.
    name : str
        The name of the workflow.
    description : str, optional
        A description of the workflow.
    kind : str, optional
        The kind of the workflow.
    spec : dict, optional
        The specification for the workflow.
    local : bool, optional
        Flag to determine if object has local execution.
    save : bool, optional
        Flag to determine if object will be saved.

    Returns
    -------
    Workflow
        An instance of the created workflow.

    """
    meta = WorkflowMetadata(name=name, description=description)
    spec = WorkflowSpec(test=test)
    obj = Workflow(
        project=project, name=name, kind=kind, metadata=meta, spec=spec, local=local
    )
    if save:
        if local:
            obj.export()
        else:
            obj.save()
    return obj


def get_workflow(project: str, name: str, uuid: str = None) -> Workflow:
    """
    Retrieves workflow details from the backend.

    Parameters
    ----------

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
    r = get_client().get_object(api)

    return Workflow.from_dict(r)


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
    d = file_importer(file)
    return Workflow.from_dict(d)


def delete_workflow(project: str, name: str, uuid: str = None) -> None:
    """
    Delete a workflow.

    Parameters
    ----------

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
    client = get_client()
    if uuid is not None:
        api = API_DELETE_VERSION.format(project, DTO_WKFL, name, uuid)
    else:
        api = API_DELETE_ALL.format(project, DTO_WKFL, name)
    return client.delete_object(api)
