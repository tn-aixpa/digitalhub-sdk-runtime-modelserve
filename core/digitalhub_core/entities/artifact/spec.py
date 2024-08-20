from __future__ import annotations

from digitalhub_core.entities._base.spec.material import MaterialParams, MaterialSpec


class ArtifactSpec(MaterialSpec):
    """
    Artifact specification.
    """


class ArtifactParams(MaterialParams):
    """
    Artifact base parameters.
    """


class ArtifactSpecArtifact(ArtifactSpec):
    """
    Artifact specification.
    """

    def __init__(
        self,
        path: str,
        src_path: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(path, **kwargs)
        self.src_path = src_path


class ArtifactParamsArtifact(ArtifactParams):
    """
    Artifact parameters.
    """

    src_path: str = None
    """Source path of the artifact."""
