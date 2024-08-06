from __future__ import annotations

from oltreai_core.entities.entity_types import EntityTypes
from oltreai_core.registry.registry import registry
from oltreai_core.registry.utils import create_info

# Root module
root = "oltreai_core.entities"

# Projects
entity_type = EntityTypes.PROJECT.value
prefix = entity_type.capitalize()
project_info = create_info(root, entity_type, prefix)
registry.register("project", project_info)


# Secrets
entity_type = EntityTypes.SECRET.value
prefix = entity_type.capitalize()
secret_info = create_info(root, entity_type, prefix)
registry.register("secret", secret_info)


# Artifacts
entity_type = EntityTypes.ARTIFACT.value
for i in ["artifact"]:
    prefix = entity_type.capitalize()
    suffix = i.capitalize()
    artifact_info = create_info(root, entity_type, prefix, suffix)
    registry.register(i, artifact_info)
