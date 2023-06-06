"""
Workflow operations module.
"""
from sdk.entities.project.context import get_context
from sdk.entities.utils import file_importer
from sdk.entities.workflow.workflow import Workflow, WorkflowMetadata, WorkflowSpec
from sdk.entities.api import (
    read_api,
    delete_api,
    DTO_WKFL,
)


def new_workflow(
    project: str,
    name: str,
    description: str = None,
    kind: str = None,
    test: str = None,
    local: bool = False,
    embed: bool = False,
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
    embed : bool, optional
        Flag to determine if object must be embedded in project.

    Returns
    -------
    Workflow
        An instance of the created workflow.

    """
    context = get_context(project)
    if context.local != local:
        raise Exception("Context local flag does not match local flag of workflow")
    meta = WorkflowMetadata(name=name, description=description)
    spec = WorkflowSpec(test=test)
    obj = Workflow(
        project=project,
        name=name,
        kind=kind,
        metadata=meta,
        spec=spec,
        local=local,
        embed=embed,
    )
    context.add_workflow(obj)
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
    context = get_context(project)
    api = read_api(project, DTO_WKFL, name, uuid=uuid)
    r = context.client.get_object(api)
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
    Delete workflow from the backend. If the uuid is not specified, delete all versions.

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
    context = get_context(project)
    api = delete_api(project, DTO_WKFL, name, uuid=uuid)
    r = context.client.delete_object(api)
    return r
