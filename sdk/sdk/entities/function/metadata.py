"""
Function metadata module.
"""
from sdk.entities.base.metadata import EntityMetadata


class FunctionMetadata(EntityMetadata):
    """
    Function metadata
    """


def build_metadata(**kwargs) -> FunctionMetadata:
    """
    Build a FunctionMetadata object with the given parameters.

    Parameters
    ----------
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    FunctionMetadata
        A FunctionMetadata object with the given parameters.
    """
    return FunctionMetadata(**kwargs)
