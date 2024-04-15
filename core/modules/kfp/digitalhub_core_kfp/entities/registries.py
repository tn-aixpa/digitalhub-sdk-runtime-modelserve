from __future__ import annotations

from digitalhub_core.entities._base.metadata import MetadataRegistry
from digitalhub_core.entities._base.spec import SpecRegistry
from digitalhub_core.entities._base.status import StatusRegistry

metadata_registry = MetadataRegistry()
status_registry = StatusRegistry()
spec_registry = SpecRegistry()

# Workflow
wf_root = "digitalhub_core_kfp.entities.workflows"
wf_kind = "kfp"
metadata_registry.register(wf_kind, f"{wf_root}.metadata", "WorkflowMetadataKFP")
spec_registry.register(wf_kind, f"{wf_root}.spec", "WorkflowSpecKFP", "WorkflowParamsKFP")
status_registry.register(wf_kind, f"{wf_root}.status", "WorkflowStatusKFP")

# Tasks
task_root = "digitalhub_core_kfp.entities.tasks"
for i in ["pipeline"]:
    task_kind = f"{wf_kind}+{i}"
    metadata_registry.register(task_kind, f"{task_root}.metadata", "TaskMetadataPipeline")
    spec_registry.register(task_kind, f"{task_root}.spec", "TaskSpecPipeline", "TaskParamsPipeline")
    status_registry.register(task_kind, f"{task_root}.status", "TaskStatusPipeline")

# Runs
run_root = "digitalhub_core_kfp.entities.runs"
run_kind = f"{wf_kind}+run"
metadata_registry.register(run_kind, f"{run_root}.metadata", "RunMetadataKFP")
spec_registry.register(run_kind, f"{run_root}.spec", "RunSpecKFP", "RunParamsKFP")
status_registry.register(run_kind, f"{run_root}.status", "RunStatusKFP")
