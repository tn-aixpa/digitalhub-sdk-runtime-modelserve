"""
Workflow metadata module.
"""
from sdk.entities.base.metadata import EntityMetadata


class WorkflowMetadata(EntityMetadata):
    """
    Workflow metadata.
    """


def build_metadata(**kwargs) -> WorkflowMetadata:
    """
    Build a WorkflowMetadata object with the given parameters.

    Parameters
    ----------
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    WorkflowMetadata
        A WorkflowMetadata object with the given parameters.
    """
    return WorkflowMetadata(**kwargs)
