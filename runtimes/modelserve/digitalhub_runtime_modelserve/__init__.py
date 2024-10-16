from __future__ import annotations

from digitalhub.entities.utils.entity_types import EntityTypes
from digitalhub.registry.registry import registry
from digitalhub.registry.utils import create_info

root = "digitalhub_runtime_modelserve"
root_ent = f"{root}.entities"

for m in ["sklearnserve", "mlflowserve", "huggingfaceserve"]:
    exec_kind = m
    suffix = exec_kind.capitalize()

    runtime_info = {
        "module": f"{root}.runtimes.runtime",
        "class_name": "RuntimeModelserve",
        "kind_registry_module": f"{root}.runtimes.kind_registry",
        "kind_registry_class_name": f"{m}_kind_registry",
    }

    # Function
    entity_type = EntityTypes.FUNCTION.value
    prefix = entity_type.capitalize()
    suffix = exec_kind.capitalize()
    exec_info = create_info(root_ent, entity_type, exec_kind, prefix, suffix, runtime_info)
    registry.register(exec_kind, exec_info)

    # Tasks
    entity_type = EntityTypes.TASK.value
    for i in ["serve"]:
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
    kind_underscore = task_kind.replace("+", "_")
    run_info = create_info(root_ent, entity_type, kind_underscore, prefix, suffix, runtime_info)
    registry.register(run_kind, run_info)
