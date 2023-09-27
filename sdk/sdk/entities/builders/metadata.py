"""
Metadata factory module.
"""
from sdk.entities.base.metadata import Metadata


def build_metadata(
    name: str | None = None, description: str | None = None, **kwargs
) -> Metadata:
    """
    Build entity metadata object.

    Parameters
    ----------
    name : str
        Name of the object.
    description : str
        Description of the entity.

    Returns
    -------
    Metadata
        An entity metadata object.
    """
    return Metadata(name=name, description=description, **kwargs)
