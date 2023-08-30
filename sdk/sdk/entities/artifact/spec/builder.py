"""
Artifact specification builder module.
"""
from sdk.entities.artifact.spec.base import ArtifactSpec
from sdk.utils.exceptions import EntityError


REGISTRY = {
    "artifact": ArtifactSpec,
    "dataset": ArtifactSpec,
}


def build_spec(kind: str, **kwargs) -> ArtifactSpec:
    """
    Build an ArtifactSpecJob object with the given parameters.

    Parameters
    ----------
    kind : str
        The type of ArtifactSpec to build.
    **kwargs : dict
        Keywords to pass to the constructor.

    Returns
    -------
    ArtifactSpec
        An ArtifactSpec object with the given parameters.

    Raises
    ------
    ValueError
        If the given kind is not supported.
    """
    try:
        return REGISTRY[kind](**kwargs)
    except KeyError:
        raise EntityError(f"Unsupported kind: {kind}")
