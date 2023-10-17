"""
Workflow specification registry module.
"""
from sdk.entities.base.spec import SpecRegistry
from sdk.entities.workflows.kinds import WorkflowKinds
from sdk.entities.workflows.spec.objects.job import WorkflowParamsJob, WorkflowSpecJob

workflow_registry = SpecRegistry()
workflow_registry.register(WorkflowKinds.WORKFLOW.value, WorkflowSpecJob, WorkflowParamsJob)
