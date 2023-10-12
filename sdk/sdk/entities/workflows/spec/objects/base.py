"""
Workflow base specification module.
"""
from pydantic import BaseModel

from sdk.entities.base.spec import EntitySpec


class WorkflowSpec(EntitySpec):
    """
    Workflow specifications.
    """

    def __init__(self, test: str | None = None) -> None:
        """
        Constructor.

        Parameters
        ----------
        test : str
            Test to run for the workflow.
        """
        self.test = test


class WorkflowParams(BaseModel):
    """
    Workflow parameters.
    """
