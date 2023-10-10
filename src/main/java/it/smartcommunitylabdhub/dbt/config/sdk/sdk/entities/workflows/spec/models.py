"""
Workflow specification models module.
"""
from pydantic import BaseModel


class WorkflowParams(BaseModel):
    """
    Workflow parameters.
    """


class WorkflowParamsJob(WorkflowParams):
    """
    Workflow job parameters.
    """

    test: str
    """Placeholder for test parameter."""
