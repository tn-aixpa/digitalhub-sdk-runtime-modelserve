from __future__ import annotations

import typing

from digitalhub_core.entities.artifacts.crud import get_artifact, get_artifact_from_key

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity import Entity
    from digitalhub_core.entities.artifacts.entity import Artifact


class EntityGetter:
    """
    Class used to collect entity objects from keys, names or dict representations.
    """

    def collect_artifacts(self, project: str, artifact_list: list[str | dict]) -> list[Artifact]:
        """
        Collect artifacts from artifact_list.

        Parameters
        ----------
        project : str
            Project name.
        artifact_list : list
            List of artifacts.

        Returns
        -------
        list
            The artifacts.
        """
        artifacts = []
        for i in artifact_list:
            if isinstance(i, str):
                if i.startswith("store://"):
                    artifacts.append(get_artifact_from_key(i))
                else:
                    artifacts.append(get_artifact(project, i))
            elif isinstance(i, dict):
                uuid = i.get("uuid")
                artifacts.append(get_artifact(project, entity_id=uuid))
            else:
                raise ValueError(f"Invalid artifact: {i}")
        return artifacts

    def collect_entity(self, object_to_parse: dict, project: str) -> dict[str, list[Entity]]:
        """
        Collect entities from object_to_parse.

        Parameters
        ----------
        object_to_parse : dict
            Object to parse.
        project : str
            Project name.

        Returns
        -------
        dict
            The entities.
        """
        entities = {}
        artifact_list = object_to_parse.get("artifacts", [])
        artifact_list = artifact_list if artifact_list is not None else []
        entities["artifacts"] = self.collect_artifacts(project, artifact_list)
        return entities
