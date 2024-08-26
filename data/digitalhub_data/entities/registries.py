from __future__ import annotations

from digitalhub_core.registry.registry import registry
from digitalhub_core.registry.utils import create_info
from digitalhub_data.entities.entity_types import EntityTypes

root = "digitalhub_data.entities"

# Projects ovverride
entity_type = EntityTypes.PROJECT.value
registry.project.spec.module = f"{root}.{entity_type}.spec"
registry.project.spec.class_name = "ProjectSpecData"
registry.project.spec.parameters_validator = "ProjectParamsData"

# Dataitems
entity_type = EntityTypes.DATAITEM.value
for i in ["dataitem", "table"]:
    prefix = entity_type.capitalize()
    suffix = i.capitalize()
    dataitem_info = create_info(root, entity_type, prefix, suffix)
    registry.register(i, dataitem_info)
