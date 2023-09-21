"""
Workflow specification registry module.
"""
from sdk.entities.workflow.kinds import WorkflowKinds
from sdk.entities.workflow.spec.models import WorkflowParamsJob
from sdk.entities.workflow.spec.objects import WorkflowSpecJob

REGISTRY_SPEC = {
    WorkflowKinds.JOB.value: WorkflowSpecJob,
}
REGISTRY_MODEL = {
    WorkflowKinds.JOB.value: WorkflowParamsJob,
}
