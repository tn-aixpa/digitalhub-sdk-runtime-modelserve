"""
RunResults module.
"""
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact


class RunResults:
    """
    A class representing a run results.
    """

    def __init__(
        self,
        artifacts: list[Artifact] | None = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        artifacts : list[Artifact]
            The artifacts.
        """
        self.artifacts = artifacts

    def get_artifacts(self) -> list[Artifact]:
        """
        Get artifacts.

        Returns
        -------
        list[Artifact]
            List of artifacts.
        """
        return self.artifacts if self.artifacts is not None else []

    def get_artifact_by_key(self, key: str) -> Artifact | None:
        """
        Get artifact by key.

        Parameters
        ----------
        key : str
            Key.

        Returns
        -------
        Artifact
            Artifact.
        """
        for artifact in self.get_artifacts():
            if artifact.name == key:
                return artifact
        return None
