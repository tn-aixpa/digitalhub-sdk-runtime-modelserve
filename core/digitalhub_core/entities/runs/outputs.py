from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact


class EntitiesOutputs:
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

    def get_artifact_by_name(self, name: str) -> Artifact | None:
        """
        Get artifact by name.

        Parameters
        ----------
        name : str
            Entity name.

        Returns
        -------
        Artifact
            Artifact.
        """
        for artifact in self.get_artifacts():
            if artifact.name == name:
                return artifact
        return None

    def list_artifact_names(self) -> list[str]:
        """
        List artifact names.

        Returns
        -------
        list[str]
            List of artifact names.
        """
        return [i.name for i in self.get_artifacts()]

    def get_artifact_by_key(self, key: str) -> Artifact | None:
        """
        Get artifact by key.

        Parameters
        ----------
        key : str
            Entity key.

        Returns
        -------
        Artifact
            Artifact.
        """
        for artifact in self.get_artifacts():
            if artifact.key == key:
                return artifact
        return None

    def list_artifact_keys(self) -> list[str]:
        """
        List artifact keys.

        Returns
        -------
        list[str]
            List of artifact keys.
        """
        return [i.key for i in self.get_artifacts()]

    def to_dict(self) -> dict:
        """
        Convert the object to a dictionary.

        Returns
        -------
        dict
            The dictionary representation of the object.
        """
        return self.__dict__

    def __repr__(self) -> str:
        return str(self.__dict__)
