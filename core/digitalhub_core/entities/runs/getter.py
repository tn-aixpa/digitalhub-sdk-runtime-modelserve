from __future__ import annotations

import typing

from digitalhub_core.entities.artifacts.crud import get_artifact, get_artifact_from_key

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity import Entity
    from digitalhub_core.entities.artifacts.entity import Artifact


class EntityGetter:
    def collect_artifacts(self, project: str, artifact_list: list[str | dict]) -> list[Artifact]:
        artifacts = []
        for i in artifact_list:
            if isinstance(i, str):
                if i.startswith("store://"):
                    artifacts.append(get_artifact_from_key(i))
                else:
                    artifacts.append(get_artifact(project, i))
            elif isinstance(i, dict):
                name = i.get("name")
                uuid = i.get("uuid")
                artifacts.append(get_artifact(project, name, uuid))
            else:
                raise ValueError(f"Invalid artifact: {i}")
        return artifacts

    def collect_entity(self, object_to_parse: dict, project: str) -> dict[list[Entity]]:
        entities = {}
        artifact_list = object_to_parse.get("artifacts", [])
        entities["artifacts"] = self.collect_artifacts(project, artifact_list)
        return entities
