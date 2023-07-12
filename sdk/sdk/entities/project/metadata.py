"""
Project metadata module.
"""
from sdk.entities.base.metadata import EntityMetadata


class ProjectMetadata(EntityMetadata):
    """
    Project metadata.
    """


def build_metadata(**kwargs) -> ProjectMetadata:
    """
    Build a ProjectMetadata object with the given parameters.

    Parameters
    ----------
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    ProjectMetadata
        A ProjectMetadata object with the given parameters.
    """
    return ProjectMetadata(**kwargs)
