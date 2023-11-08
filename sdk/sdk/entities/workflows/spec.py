"""
Workflow base specification module.
"""
from pydantic import BaseModel

from sdk.entities._base.spec import Spec


class WorkflowSpec(Spec):
    """
    Workflow specifications.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """


class WorkflowParams(BaseModel):
    """
    Workflow parameters.
    """
