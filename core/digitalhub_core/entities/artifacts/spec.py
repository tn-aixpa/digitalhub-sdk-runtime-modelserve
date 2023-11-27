"""
Artifact base specification module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.spec import Spec
from pydantic import BaseModel


class ArtifactSpec(Spec):
    """
    Artifact specification.
    """

    def __init__(
        self,
        key: str | None = None,
        src_path: str | None = None,
        target_path: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        key : str
            The key of the artifact.
        src_path : str
            The source path of the artifact.
        target_path : str
            The target path of the artifact.
        **kwargs
            Keywords arguments.
        """
        self.key = key
        self.src_path = src_path
        self.target_path = target_path

        self._any_setter(**kwargs)


class ArtifactParams(BaseModel):
    """
    Artifact base parameters.
    """

    key: str = None
    """Key of the artifact"""

    src_path: str = None
    """Source path of the artifact."""

    target_path: str = None
    """Target path of the artifact."""
