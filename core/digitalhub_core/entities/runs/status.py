"""
RunStatus class module.
"""
from __future__ import annotations

import typing

from digitalhub_core.entities._base.entity import Entity
from digitalhub_core.entities._base.status import Status
from digitalhub_core.entities.artifacts.crud import get_artifact, get_artifact_from_key

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact


OUTPUTS_ENTITIES = ["artifacts"]
ENTITIES_GETTERS = {
    "artifacts": {
        "key": get_artifact_from_key,
        "name": get_artifact,
        "object": get_artifact,
    }
}


class RunStatus(Status):
    """
    Status class for run entities.
    """

    def __init__(self, state: str, message: str | None = None) -> None:
        super().__init__(state, message)
        self.outputs: dict | None = None
        self.results: dict | None = None

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

    def get_outputs(self) -> dict:
        """
        Get results.

        Returns
        -------
        dict
            The results.
        """
        artifacts = self.outputs.get("artifacts", [])
        # TODO: get artifacts
        # Key, name, dict

        artifact_objs = [get_artifact_from_key(art.get("id")) for art in artifacts]
        return EntitiesOutputs(artifacts=artifact_objs)


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

    def __repr__(self) -> str:
        return str(self.__dict__)


def get_entity_info(entity: Entity, entity_type: str) -> dict:
    """
    Get the information of an entity.

    Parameters
    ----------
    entity : entity
        The entity object.
    entity_type : str
        The type of the entity.

    Returns
    -------
    dict
        The information of the entity.
    """
    return {
        "id": f"store://{entity.project}/{entity_type}/{entity.kind}/{entity.name}:{entity.id}",
        "name": entity.name,
    }
