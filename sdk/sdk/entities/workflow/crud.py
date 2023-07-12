"""
Workflow operations module.
"""
from __future__ import annotations

import typing

from sdk.entities.utils.utils import check_local_flag, save_or_export
from sdk.entities.workflow.entity import workflow_from_dict, workflow_from_parameters
from sdk.utils.api import DTO_WKFL, api_ctx_delete, api_ctx_read
from sdk.utils.factories import get_context
from sdk.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from sdk.entities.workflow.entity import Workflow


def create_workflow(
    project: str,
    name: str,
    description: str = "",
    kind: str = "job",
    test: str = None,
    local: bool = False,
    embedded: bool = False,
    uuid: str = None,
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
    embedded : bool, optional
        Flag to determine if object must be embedded in project.
    uuid : str, optional
        UUID.

    Returns
    -------
    Workflow
        An instance of the created workflow.

    """
    return workflow_from_parameters(
        project=project,
        name=name,
        description=description,
        kind=kind,
        test=test,
        local=local,
        embedded=embedded,
        uuid=uuid,
    )


def create_workflow_from_dict(obj: dict) -> Workflow:
    """
    Create a new Workflow instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create the Workflow from.

    Returns
    -------
    Workflow
        Workflow object.
    """
    return workflow_from_dict(obj)


def new_workflow(
    project: str,
    name: str,
    description: str = "",
    kind: str = "job",
    test: str = None,
    local: bool = False,
    embedded: bool = False,
    uuid: str = None,
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
    embedded : bool, optional
        Flag to determine if object must be embedded in project.
    uuid : str, optional
        UUID.

    Returns
    -------
    Workflow
        An instance of the created workflow.

    """
    check_local_flag(project, local)
    obj = create_workflow(
        project=project,
        name=name,
        description=description,
        kind=kind,
        test=test,
        local=local,
        embedded=embedded,
        uuid=uuid,
    )
    save_or_export(obj, local)
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
    api = api_ctx_read(project, DTO_WKFL, name, uuid=uuid)
    obj = get_context(project).read_object(api)
    return workflow_from_dict(obj)


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
    return workflow_from_dict(obj)


def delete_workflow(project: str, name: str, uuid: str = None) -> dict:
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
    dict
        Response from backend.
    """
    api = api_ctx_delete(project, DTO_WKFL, name, uuid=uuid)
    return get_context(project).delete_object(api)
