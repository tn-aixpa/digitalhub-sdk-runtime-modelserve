from __future__ import annotations

from digitalhub.entities._base.spec.material import MaterialSpec, MaterialValidator


class ArtifactSpec(MaterialSpec):
    """
    Artifact specification.
    """


class ArtifactValidator(MaterialValidator):
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


class ArtifactValidatorArtifact(ArtifactValidator):
    """
    Artifact parameters.
    """

    src_path: str = None
    """Source path of the artifact."""
