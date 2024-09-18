from __future__ import annotations

from digitalhub_core.registry.registry import registry
from digitalhub_core.registry.utils import create_info
from digitalhub_ml.entities.entity_types import EntityTypes

root = "digitalhub_runtime_kfp"
runtime_info = {
    "module": f"{root}.runtimes.runtime",
    "class_name": "RuntimeKFP",
    "kind_registry_module": f"{root}.runtimes.kind_registry",
    "kind_registry_class_name": "kind_registry",
}

root_ent = f"{root}.entities"

# Workflow
entity_type = EntityTypes.WORKFLOW.value
wkfl_kind = "kfp"
prefix = entity_type.capitalize()
suffix = wkfl_kind.upper()
wkfl_info = create_info(root_ent, entity_type, prefix, suffix, runtime_info)
registry.register(wkfl_kind, wkfl_info)


# Tasks
entity_type = EntityTypes.TASK.value
for i in ["pipeline", "build"]:
    task_kind = f"{wkfl_kind}+{i}"
    prefix = entity_type.capitalize()
    suffix = i.capitalize()
    task_info = create_info(root_ent, entity_type, prefix, suffix, runtime_info)
    registry.register(task_kind, task_info)


# Runs
entity_type = EntityTypes.RUN.value
run_kind = f"{wkfl_kind}+run"
prefix = entity_type.capitalize()
suffix = wkfl_kind.upper()
run_info = create_info(root_ent, entity_type, prefix, suffix, runtime_info)
registry.register(run_kind, run_info)
