"""
Workflow operations module.
"""
from sdk.entities.workflow.entity import Workflow
from sdk.entities.workflow.metadata import WorkflowMetadata
from sdk.entities.workflow.spec import WorkflowSpec
from sdk.utils.api import DTO_WKFL, api_ctx_delete, api_ctx_read
from sdk.utils.exceptions import EntityError
from sdk.utils.factories import get_context
from sdk.utils.io_utils import read_yaml


def new_workflow(
    project: str,
    name: str,
    description: str = None,
    kind: str = None,
    test: str = None,
    local: bool = False,
    embed: bool = False,
    **kwargs,
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
    **kwargs
        Additional keyword arguments.

    Returns
    -------
    Workflow
        An instance of the created workflow.

    """
    context = get_context(project)
    if context.local != local:
        raise EntityError("Context local flag does not match local flag of workflow")
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
        **kwargs,
    )
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
    """
    context = get_context(project)
    api = api_ctx_read(project, DTO_WKFL, name, uuid=uuid)
    obj = context.read_object(api)
    return Workflow.from_dict(obj)


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
    obj = read_yaml(file)
    return Workflow.from_dict(obj)


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
    api = api_ctx_delete(project, DTO_WKFL, name, uuid=uuid)
    return context.delete_object(api)
