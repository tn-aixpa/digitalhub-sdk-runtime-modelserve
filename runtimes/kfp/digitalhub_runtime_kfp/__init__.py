from __future__ import annotations

from digitalhub.entities.utils.entity_types import EntityTypes
from digitalhub.registry.registry import registry
from digitalhub.registry.utils import create_info

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
exec_kind = "kfp"
prefix = entity_type.capitalize()
suffix = exec_kind.capitalize()
exec_info = create_info(root_ent, entity_type, exec_kind, prefix, suffix, runtime_info)
registry.register(exec_kind, exec_info)


# Tasks
entity_type = EntityTypes.TASK.value
for i in ["pipeline"]:
    task_kind = f"{exec_kind}+{i}"
    prefix = entity_type.capitalize()
    suffix = exec_kind.capitalize() + i.capitalize()
    kind_underscore = task_kind.replace("+", "_")
    task_info = create_info(root_ent, entity_type, kind_underscore, prefix, suffix, runtime_info)
    registry.register(task_kind, task_info)


# Runs
entity_type = EntityTypes.RUN.value
run_kind = f"{exec_kind}+run"
prefix = entity_type.capitalize()
suffix = exec_kind.capitalize() + entity_type.capitalize()
kind_underscore = run_kind.replace("+", "_")
run_info = create_info(root_ent, entity_type, kind_underscore, prefix, suffix, runtime_info)
registry.register(run_kind, run_info)
