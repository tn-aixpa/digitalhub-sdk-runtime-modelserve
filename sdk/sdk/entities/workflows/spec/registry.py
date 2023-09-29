"""
Workflow specification registry module.
"""
from sdk.entities.workflows.kinds import WorkflowKinds
from sdk.entities.workflows.spec.models import WorkflowParamsJob
from sdk.entities.workflows.spec.objects import WorkflowSpecJob

WORKFLOW_SPEC = {
    WorkflowKinds.WORKFLOW.value: WorkflowSpecJob,
}
WORKFLOW_MODEL = {
    WorkflowKinds.WORKFLOW.value: WorkflowParamsJob,
}
