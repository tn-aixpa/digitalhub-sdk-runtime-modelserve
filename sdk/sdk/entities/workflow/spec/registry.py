"""
Workflow specification registry module.
"""
from sdk.entities.workflow.kinds import WorkflowKinds
from sdk.entities.workflow.spec.models import WorkflowParamsJob
from sdk.entities.workflow.spec.objects import WorkflowSpecJob

WORKFLOW_SPEC = {
    WorkflowKinds.WORKFLOW.value: WorkflowSpecJob,
}
WORKFLOW_MODEL = {
    WorkflowKinds.WORKFLOW.value: WorkflowParamsJob,
}
