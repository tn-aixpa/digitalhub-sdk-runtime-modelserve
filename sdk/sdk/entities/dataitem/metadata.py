"""
Dataitem metadata module.
"""
from sdk.entities.base.metadata import EntityMetadata


class DataitemMetadata(EntityMetadata):
    """
    Dataitem metadata.
    """


def build_metadata(**kwargs) -> DataitemMetadata:
    """
    Build a DataitemMetadata object with the given parameters.

    Parameters
    ----------
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    DataitemMetadata
        A DataitemMetadata object with the given parameters.
    """
    return DataitemMetadata(**kwargs)
