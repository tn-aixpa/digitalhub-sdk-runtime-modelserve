"""
Artifact specification models module.
"""
from pydantic import BaseModel


class ArtifactParams(BaseModel):
    """
    Artifact base parameters.
    """

    key: str | None = None
    """Key of the artifact"""

    src_path: str | None = None
    """Source path of the artifact."""

    target_path: str | None = None
    """Target path of the artifact."""


class ArtifactParamsArtifact(ArtifactParams):
    """
    Artifact kind Artifact parameters.
    """
