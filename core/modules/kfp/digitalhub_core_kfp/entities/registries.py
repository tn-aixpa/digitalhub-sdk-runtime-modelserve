from __future__ import annotations

from digitalhub_core.entities._base.metadata import MetadataRegistry
from digitalhub_core.entities._base.spec import SpecRegistry
from digitalhub_core.entities._base.status import StatusRegistry

metadata_registry = MetadataRegistry()
status_registry = StatusRegistry()
spec_registry = SpecRegistry()

# Function
func_root = "digitalhub_core_kfp.entities.functions"
func_kind = "kfp"
metadata_registry.register(func_kind, f"{func_root}.metadata", "FunctionMetadataKFP")
spec_registry.register(func_kind, f"{func_root}.spec", "FunctionSpecKFP", "FunctionParamsKFP")
status_registry.register(func_kind, f"{func_root}.status", "FunctionStatusKFP")

# Tasks
task_root = "digitalhub_core_kfp.entities.tasks"
for i in ["pipeline"]:
    task_kind = f"{func_kind}+{i}"
    metadata_registry.register(task_kind, f"{task_root}.metadata", f"TaskMetadataPipeline")
    spec_registry.register(task_kind, f"{task_root}.spec", f"TaskSpecPipeline", f"TaskParamsPipeline")
    status_registry.register(task_kind, f"{task_root}.status", f"TaskStatusPipeline")

# Runs
run_root = "digitalhub_core_kfp.entities.runs"
run_kind = f"{func_kind}+run"
metadata_registry.register(run_kind, f"{run_root}.metadata", "RunMetadataKFP")
spec_registry.register(run_kind, f"{run_root}.spec", "RunSpecKFP", "RunParamsKFP")
status_registry.register(run_kind, f"{run_root}.status", "RunStatusKFP")
