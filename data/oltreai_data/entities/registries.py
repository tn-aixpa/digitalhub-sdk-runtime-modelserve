from __future__ import annotations

from oltreai_core.registry.registry import registry
from oltreai_core.registry.utils import create_info
from oltreai_data.entities.entity_types import EntityTypes

root = "oltreai_data.entities"

# Projects ovverride
entity_type = EntityTypes.PROJECT.value
registry.project.spec.module = f"{root}.{entity_type}.spec"
registry.project.spec.class_name = "ProjectSpecData"
registry.project.spec.parameters_validator = "ProjectParamsData"

# Dataitems
entity_type = EntityTypes.DATAITEM.value
for i in ["dataitem", "table", "iceberg"]:
    prefix = entity_type.capitalize()
    suffix = i.capitalize()
    dataitem_info = create_info(root, entity_type, prefix, suffix)
    registry.register(i, dataitem_info)
