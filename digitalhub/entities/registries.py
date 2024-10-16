from __future__ import annotations

from digitalhub.entities.utils.entity_types import EntityTypes
from digitalhub.registry.registry import registry
from digitalhub.registry.utils import create_info

# Root module
root = "digitalhub.entities"

# Projects
entity_type = EntityTypes.PROJECT.value
prefix = entity_type.capitalize()
project_info = create_info(root, entity_type, "project", prefix)
registry.register("project", project_info)


# Secrets
entity_type = EntityTypes.SECRET.value
prefix = entity_type.capitalize()
secret_info = create_info(root, entity_type, "secret", prefix)
registry.register("secret", secret_info)


# Artifacts
entity_type = EntityTypes.ARTIFACT.value
for i in ["artifact"]:
    prefix = entity_type.capitalize()
    suffix = i.capitalize()
    artifact_info = create_info(root, entity_type, i, prefix, suffix)
    registry.register(i, artifact_info)


# Dataitems
entity_type = EntityTypes.DATAITEM.value
for i in ["dataitem", "table"]:
    prefix = entity_type.capitalize()
    suffix = i.capitalize()
    dataitem_info = create_info(root, entity_type, i, prefix, suffix)
    registry.register(i, dataitem_info)


# Models
entity_type = EntityTypes.MODEL.value
for i in ["model", "mlflow", "sklearn", "huggingface"]:
    prefix = entity_type.capitalize()
    suffix = i.capitalize()
    model_info = create_info(root, entity_type, i, prefix, suffix)
    registry.register(i, model_info)
