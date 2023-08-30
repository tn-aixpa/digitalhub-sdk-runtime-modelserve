"""
Project specification builder module.
"""
from sdk.entities.project.spec.base import ProjectSpec
from sdk.utils.exceptions import EntityError


REGISTRY = {
    "project": ProjectSpec,
}


def build_spec(kind: str, **kwargs) -> ProjectSpec:
    """
    Build a ProjectSpec object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of ProjectSpec to build.
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    ProjectSpec
        A ProjectSpec object with the given parameters.

    Raises
    ------
    ValueError
        If the given kind is not supported.
    """
    try:
        return REGISTRY[kind](**kwargs)
    except KeyError:
        raise EntityError(f"Unsupported kind: {kind}")
