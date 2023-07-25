"""
Artifact metadata module.
"""
from sdk.entities.base.metadata import EntityMetadata


class ArtifactMetadata(EntityMetadata):
    """
    Artifact metadata.
    """


def build_metadata(**kwargs) -> ArtifactMetadata:
    """
    Build an ArtifactMetadata object with the given parameters.

    Parameters
    ----------
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    ArtifactMetadata
        An ArtifactMetadata object with the given parameters.
    """
    return ArtifactMetadata(**kwargs)
