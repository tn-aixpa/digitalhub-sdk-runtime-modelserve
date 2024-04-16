from __future__ import annotations

from digitalhub_core.entities.entity_types import EntityType
from digitalhub_core.registry.registry import registry

runtime_info = {
    "module": "digitalhub_core_kfp.runtimes.runtime",
    "class_name": "RuntimeKFP",
}

root = "digitalhub_core_kfp.entities"

# Workflow
wkfl_kind = "kfp"
entity_type = "workflows"
wkfl_info = {
    "entity_type": entity_type,
    "spec": {
        "module": f"{root}.{entity_type}.spec",
        "class_name": f"WorkflowSpec{wkfl_kind.upper()}",
        "parameters_validator": f"WorkflowParams{wkfl_kind.upper()}",
    },
    "status": {
        "module": f"{root}.{entity_type}.status",
        "class_name": f"WorkflowStatus{wkfl_kind.upper()}",
    },
    "metadata": {
        "module": f"{root}.{entity_type}.metadata",
        "class_name": f"WorkflowMetadata{wkfl_kind.upper()}",
    },
    "runtime": runtime_info,
}
registry.register(wkfl_kind, wkfl_info)


# Tasks
entity_type = "tasks"
for i in ["pipeline"]:
    task_kind = f"{wkfl_kind}+{i}"
    task_info = {
        "entity_type": entity_type,
        "spec": {
            "module": f"{root}.{entity_type}.spec",
            "class_name": f"TaskSpec{i.title()}",
            "parameters_validator": f"TaskParams{i.title()}",
        },
        "status": {
            "module": f"{root}.{entity_type}.status",
            "class_name": f"TaskStatus{i.title()}",
        },
        "metadata": {
            "module": f"{root}.{entity_type}.metadata",
            "class_name": f"TaskMetadata{i.title()}",
        },
        "runtime": runtime_info,
    }
    registry.register(task_kind, task_info)


# Runs
run_kind = f"{wkfl_kind}+run"
entity_type = "runs"
run_info = {
    "entity_type": entity_type,
    "spec": {
        "module": f"{root}.{entity_type}.spec",
        "class_name": f"RunSpec{wkfl_kind.upper()}",
        "parameters_validator": f"RunParams{wkfl_kind.upper()}",
    },
    "status": {
        "module": f"{root}.{entity_type}.status",
        "class_name": f"RunStatus{wkfl_kind.upper()}",
    },
    "metadata": {
        "module": f"{root}.{entity_type}.metadata",
        "class_name": f"RunMetadata{wkfl_kind.upper()}",
    },
    "runtime": runtime_info,
}
registry.register(run_kind, run_info)
