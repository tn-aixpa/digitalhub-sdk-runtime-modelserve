"""
Workflow kind enum module.
"""
from enum import Enum

from sdk.entities.base.kinds import kind_builder


class WorkflowKinds(Enum):
    """
    Workflow kind enum class.
    """

    JOB = "job"


def build_kind(kind: str | None = None) -> str:
    """
    Build workflow kind.

    Parameters
    ----------
    kind : str
        Kind to check. If None, return default kind.

    Returns
    -------
    str
        Workflow kind.
    """
    return kind_builder(WorkflowKinds, WorkflowKinds.JOB.value, kind)
