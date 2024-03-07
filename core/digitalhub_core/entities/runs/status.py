"""
RunStatus class module.
"""
from __future__ import annotations

import typing

from digitalhub_core.entities._base.status import Status
from digitalhub_core.entities.runs.getter import EntityGetter

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact


class RunStatus(Status):
    """
    Status class for run entities.
    """

    def __init__(self, state: str, message: str | None = None, outputs: dict | None = None, results: dict | None = None) -> None:
        """
        Constructor.

        Parameters
        ----------
        state : str
            The state of the entity.
        message : str
            Error message.
        """
        super().__init__(state, message)
        self.outputs = outputs
        self.results = results

    # TODO: abstractmethod to be implemented by runtimes
    def get_results(self) -> dict:
        """
        Get results.

        Returns
        -------
        dict
            The results.
        """
        return self.results if self.results is not None else {}

    def get_outputs(self, project_name: str) -> EntitiesOutputs:
        """
        Get results.

        Returns
        -------
        dict
            The results.
        """
        outputs = EntityGetter().collect_entity(self.outputs, project_name)
        return EntitiesOutputs(**outputs)


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
