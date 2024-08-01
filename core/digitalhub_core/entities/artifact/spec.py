from __future__ import annotations

from digitalhub_core.entities._base.spec.material import MaterialParams, MaterialSpec


class ArtifactSpec(MaterialSpec):
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


class ArtifactParams(MaterialParams):
    """
    Artifact base parameters.
    """

    src_path: str = None
    """Source path of the artifact."""


class ArtifactSpecArtifact(ArtifactSpec):
    """
    Artifact specification.
    """


class ArtifactParamsArtifact(ArtifactParams):
    """
    Artifact parameters.
    """
