from __future__ import annotations

import typing

from digitalhub_core.entities.runs.getter import EntityGetter
from digitalhub_data.entities.dataitems.crud import get_dataitem, get_dataitem_from_key

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity import Entity
    from digitalhub_data.entities.dataitems.entity._base import Dataitem


class EntityGetterData(EntityGetter):
    def collect_dataitems(self, project: str, dataitem_list: list[str | dict]) -> list[Dataitem]:
        dataitems = []
        for i in dataitem_list:
            if isinstance(i, str):
                if i.startswith("store://"):
                    dataitems.append(get_dataitem_from_key(i))
                else:
                    dataitems.append(get_dataitem(project, i))
            elif isinstance(i, dict):
                name = i.get("name")
                uuid = i.get("uuid")
                dataitems.append(get_dataitem(project, name, uuid))
            else:
                raise ValueError(f"Invalid dataitem: {i}")
        return dataitems

    def collect_entity(self, object_to_parse: dict, project: str) -> dict[list[Entity]]:
        entities = super().collect_entity(object_to_parse, project)
        dataitem_list = object_to_parse.get("dataitems", [])
        entities["dataitems"] = self.collect_dataitems(project, dataitem_list)
        return entities
