"""
Job Workflow specification module.
"""
from sdk.entities.workflows.spec.objects.base import WorkflowParams, WorkflowSpec


class WorkflowSpecJob(WorkflowSpec):
    """
    Specification for a Workflow job.
    """


class WorkflowParamsJob(WorkflowParams):
    """
    Workflow job parameters.
    """

    test: str
    """Placeholder for test parameter."""
