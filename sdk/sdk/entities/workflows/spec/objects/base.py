"""
Workflow base specification module.
"""
from pydantic import BaseModel

from sdk.entities.base.spec import Spec


class WorkflowSpec(Spec):
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
