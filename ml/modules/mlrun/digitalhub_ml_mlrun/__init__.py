from __future__ import annotations

from digitalhub_core.entities.entity_types import EntityType
from digitalhub_core.registry.registry import registry

root = "digitalhub_ml_mlrun"
runtime_info = {
    "module": f"{root}.runtimes.runtime",
    "class_name": "RuntimeMlrun",
}

root_ent = f"{root}.entities"

# Function
func_kind = "mlrun"
entity_type = "functions"
func_info = {
    "entity_type": entity_type,
    "spec": {
        "module": f"{root_ent}.{entity_type}.spec",
        "class_name": f"FunctionSpec{func_kind.title()}",
        "parameters_validator": f"FunctionParams{func_kind.title()}",
    },
    "status": {
        "module": f"{root_ent}.{entity_type}.status",
        "class_name": f"FunctionStatus{func_kind.title()}",
    },
    "metadata": {
        "module": f"{root_ent}.{entity_type}.metadata",
        "class_name": f"FunctionMetadata{func_kind.title()}",
    },
    "runtime": runtime_info,
}
registry.register(func_kind, func_info)


# Tasks
entity_type = "tasks"
for i in ["job"]:
    task_kind = f"{func_kind}+{i}"
    task_info = {
        "entity_type": entity_type,
        "spec": {
            "module": f"{root_ent}.{entity_type}.spec",
            "class_name": f"TaskSpec{i.title()}",
            "parameters_validator": f"TaskParams{i.title()}",
        },
        "status": {
            "module": f"{root_ent}.{entity_type}.status",
            "class_name": f"TaskStatus{i.title()}",
        },
        "metadata": {
            "module": f"{root_ent}.{entity_type}.metadata",
            "class_name": f"TaskMetadata{i.title()}",
        },
        "runtime": runtime_info,
    }
    registry.register(task_kind, task_info)


# Runs
run_kind = f"{func_kind}+run"
entity_type = "runs"
run_info = {
    "entity_type": entity_type,
    "spec": {
        "module": f"{root_ent}.{entity_type}.spec",
        "class_name": f"RunSpec{func_kind.title()}",
        "parameters_validator": f"RunParams{func_kind.title()}",
    },
    "status": {
        "module": f"{root_ent}.{entity_type}.status",
        "class_name": f"RunStatus{func_kind.title()}",
    },
    "metadata": {
        "module": f"{root_ent}.{entity_type}.metadata",
        "class_name": f"RunMetadata{func_kind.title()}",
    },
    "runtime": runtime_info,
}
registry.register(run_kind, run_info)
