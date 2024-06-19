"""
Artifact base specification module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.spec import Spec, SpecParams


class ArtifactSpec(Spec):
    """
    Artifact specification.
    """

    def __init__(
        self,
        path: str | None = None,
        src_path: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        path : str
            The target path of the artifact.
        src_path : str
            The source path of the artifact.
        hash : str
            The hash of the artifact.
        size : int
            The size of the artifact.
        content_type : str
            The mimetype of the artifact.
        file_extension : str
            The file extension of the artifact.
        **kwargs
            Keywords arguments.
        """
        self.path = path
        self.src_path = src_path

        self._any_setter(**kwargs)


class ArtifactParams(SpecParams):
    """
    Artifact base parameters.
    """

    path: str = None
    """Target path of the artifact."""

    src_path: str = None
    """Source path of the artifact."""

    hash: str = None
    """Hash of the artifact."""

    size: int = None
    """Size of the artifact."""

    content_type: str = None
    """Mimetype of the artifact."""

    file_extension: str = None
    """File extension of the artifact."""


class ArtifactSpecArtifact(ArtifactSpec):
    """
    Artifact specification.
    """


class ArtifactParamsArtifact(ArtifactParams):
    """
    Artifact parameters.
    """
