"""
Workflow base specification module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.spec import Spec
from pydantic import BaseModel


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
