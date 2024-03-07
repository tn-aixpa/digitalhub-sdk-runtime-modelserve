from __future__ import annotations

from digitalhub_core.entities._base.metadata import MetadataRegistry
from digitalhub_core.entities._base.spec import SpecRegistry
from digitalhub_core.entities._base.status import StatusRegistry

metadata_registry = MetadataRegistry()
spec_registry = SpecRegistry()
status_registry = StatusRegistry()

# Function
func_root = "digitalhub_data_dbt.entities.functions"
func_kind = "dbt"
metadata_registry.register(func_kind, f"{func_root}.metadata", "FunctionMetadataDbt")
spec_registry.register(func_kind, f"{func_root}.spec", "FunctionSpecDbt", "FunctionParamsDbt")
status_registry.register(func_kind, f"{func_root}.status", "FunctionStatusDbt")

# Tasks
task_root = "digitalhub_data_dbt.entities.tasks"
for i in ["transform"]:
    task_kind = f"{func_kind}+{i}"
    metadata_registry.register(task_kind, f"{task_root}.metadata", f"TaskMetadata{i.title()}")
    spec_registry.register(task_kind, f"{task_root}.spec", f"TaskSpec{i.title()}", f"TaskParams{i.title()}")
    status_registry.register(task_kind, f"{task_root}.status", f"TaskStatus{i.title()}")

# Runs
run_root = "digitalhub_data_dbt.entities.runs"
run_kind = f"{func_kind}+run"
metadata_registry.register(run_kind, f"{run_root}.metadata", "RunMetadataDbt")
spec_registry.register(run_kind, f"{run_root}.spec", "RunSpecDbt", "RunParamsDbt")
status_registry.register(run_kind, f"{run_root}.status", "RunStatusDbt")
