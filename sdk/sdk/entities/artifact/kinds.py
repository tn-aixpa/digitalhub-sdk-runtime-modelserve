"""
Artifact kind enum module.
"""
from enum import Enum

from sdk.entities.base.kinds import kind_builder


class ArtifactKinds(Enum):
    """
    Artifact kind enum class.
    """

    ARTIFACT = "artifact"


def build_kind(kind: str | None = None) -> str:
    """
    Build artifact kind.

    Parameters
    ----------
    kind : str
        Kind to check. If None, return default kind.

    Returns
    -------
    str
        Artifact kind.
    """
    return kind_builder(ArtifactKinds, ArtifactKinds.ARTIFACT.value, kind)
