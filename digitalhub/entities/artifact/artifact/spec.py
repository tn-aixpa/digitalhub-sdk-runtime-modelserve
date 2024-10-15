from __future__ import annotations

from digitalhub.entities.artifact._base.spec import ArtifactSpec, ArtifactValidator


class ArtifactSpecArtifact(ArtifactSpec):
    """
    Artifact specifications.
    """

    def __init__(
        self,
        path: str,
        src_path: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(path, **kwargs)
        self.src_path = src_path


class ArtifactValidatorArtifact(ArtifactValidator):
    """
    Artifact parameters.
    """

    src_path: str = None
    """Source path of the artifact."""
