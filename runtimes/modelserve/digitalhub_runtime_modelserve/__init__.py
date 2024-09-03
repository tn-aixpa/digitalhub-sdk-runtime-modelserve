from __future__ import annotations

from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.registry.registry import registry
from digitalhub_core.registry.utils import create_info

root = "digitalhub_runtime_modelserve"
root_ent = f"{root}.entities"

for m in ["sklearnserve", "mlflowserve", "huggingfaceserve"]:
    func_kind = m
    suffix = func_kind.capitalize()

    runtime_info = {
        "module": f"{root}.runtimes.runtime",
        "class_name": "RuntimeModelserve",
        "kind_registry_module": f"{root}.runtimes.kind_registry",
        "kind_registry_class_name": f"{m}_kind_registry",
    }

    # Function
    entity_type = EntityTypes.FUNCTION.value
    prefix = entity_type.capitalize()
    suffix = func_kind.capitalize()
    func_info = create_info(root_ent, entity_type, prefix, suffix, runtime_info)
    registry.register(func_kind, func_info)

    # Tasks
    entity_type = EntityTypes.TASK.value
    for i in ["serve"]:
        task_kind = f"{func_kind}+{i}"
        prefix = entity_type.capitalize()
        suffix = func_kind.capitalize() + i.capitalize()
        task_info = create_info(root_ent, entity_type, prefix, suffix, runtime_info)
        registry.register(task_kind, task_info)

    # Runs
    entity_type = EntityTypes.RUN.value
    run_kind = f"{func_kind}+run"
    prefix = entity_type.capitalize()
    suffix = func_kind.capitalize()
    run_info = create_info(root_ent, entity_type, prefix, suffix, runtime_info)
    registry.register(run_kind, run_info)
