"""
ArtifactStatus class module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.status import Status


class ArtifactStatus(Status):
    """
    Status class for artifact entities.
    """


class ArtifactStatusArtifact(ArtifactStatus):
    """
    Status class for artifact entities.
    """

    def __init__(
        self,
        state: str,
        message: str | None = None,
        hash: str | None = None,
        size: int | None = None,
        content_type: str | None = None,
        file_extension: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        **kwargs
            Keywords arguments.
        """
        super().__init__(state, message)
        self.hash = hash
        self.size = size
        self.content_type = content_type
        self.file_extension = file_extension
