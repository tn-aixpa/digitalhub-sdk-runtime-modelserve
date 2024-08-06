from __future__ import annotations

from oltreai_core.registry.registry import registry
from oltreai_core.registry.utils import create_info
from oltreai_ml.entities.entity_types import EntityTypes

root = "oltreai_ml.entities"

# Projects ovverride
entity_type = EntityTypes.PROJECT.value
registry.project.spec.module = f"{root}.{entity_type}.spec"
registry.project.spec.class_name = "ProjectSpecMl"
registry.project.spec.parameters_validator = "ProjectParamsMl"

# Models
entity_type = EntityTypes.MODEL.value
for i in ["model", "mlflow", "pickle", "huggingface"]:
    prefix = entity_type.capitalize()
    suffix = i.capitalize()
    model_info = create_info(root, entity_type, prefix, suffix)
    registry.register(i, model_info)
