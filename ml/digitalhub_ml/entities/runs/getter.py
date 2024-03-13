from __future__ import annotations

import typing

from digitalhub_data.entities.runs.getter import EntityGetterData
from digitalhub_ml.entities.models.crud import get_model, get_model_from_key

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity import Entity
    from digitalhub_ml.entities.models.entity import Model


class EntityGetterMl(EntityGetterData):
    def collect_models(self, project: str, model_list: list[str | dict]) -> list[Model]:
        models = []
        for i in model_list:
            if isinstance(i, str):
                if i.startswith("store://"):
                    models.append(get_model_from_key(i))
                else:
                    models.append(get_model(project, i))
            elif isinstance(i, dict):
                uuid = i.get("uuid")
                models.append(get_model(project, entity_id=uuid))
            else:
                raise ValueError(f"Invalid model: {i}")
        return models

    def collect_entity(self, object_to_parse: dict, project: str) -> dict[str, list[Entity]]:
        entities = super().collect_entity(object_to_parse, project)
        model_list = object_to_parse.get("models", [])
        entities["models"] = self.collect_models(project, model_list)
        return entities
