from __future__ import annotations

from digitalhub_core.entities._base.metadata import MetadataRegistry
from digitalhub_core.entities._base.spec import SpecRegistry
from digitalhub_core.entities._base.status import StatusRegistry

metadata_registry = MetadataRegistry()
spec_registry = SpecRegistry()
status_registry = StatusRegistry()

# Function
func_root = "digitalhub_core_container.entities.functions"
func_kind = "container"
metadata_registry.register(func_kind, f"{func_root}.metadata", "FunctionMetadataContainer")
spec_registry.register(func_kind, f"{func_root}.spec", "FunctionSpecContainer", "FunctionParamsContainer")
status_registry.register(func_kind, f"{func_root}.status", "FunctionStatusContainer")

# Tasks
task_root = "digitalhub_core_container.entities.tasks"
for i in ["job", "serve", "deploy"]:
    task_kind = f"{func_kind}+{i}"
    metadata_registry.register(task_kind, f"{task_root}.metadata", f"TaskMetadata{i.title()}")
    spec_registry.register(task_kind, f"{task_root}.spec", f"TaskSpec{i.title()}", f"TaskParams{i.title()}")
    status_registry.register(task_kind, f"{task_root}.status", f"TaskStatus{i.title()}")

# Runs
run_root = "digitalhub_core_container.entities.runs"
run_kind = f"{func_kind}+run"
metadata_registry.register(run_kind, f"{run_root}.metadata", "RunMetadataContainer")
spec_registry.register(run_kind, f"{run_root}.spec", "RunSpecContainer", "RunParamsContainer")
status_registry.register(run_kind, f"{run_root}.status", "RunStatusContainer")
