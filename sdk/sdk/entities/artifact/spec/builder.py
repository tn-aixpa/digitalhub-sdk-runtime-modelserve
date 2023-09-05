"""
Artifact specification builder module.
"""
from sdk.entities.artifact.spec.base import ArtifactSpec
from sdk.utils.exceptions import EntityError


REGISTRY_SPEC = {
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
    **kwargs
        Keywords arguments.

    Returns
    -------
    ArtifactSpec
        An ArtifactSpec object with the given parameters.

    Raises
    ------
    EntityError
        If the given kind is not supported.
    """
    try:
        return REGISTRY_SPEC[kind](**kwargs)
    except KeyError:
        raise EntityError(f"Unsupported kind: {kind}")
