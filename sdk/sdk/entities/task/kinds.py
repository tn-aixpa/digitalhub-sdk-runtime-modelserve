"""
Task kind enum module.
"""
from enum import Enum

from sdk.entities.base.kinds import kind_builder


class TaskKinds(Enum):
    """
    Task kind enum class.
    """

    JOB = "perform"
    BUILD = "build"
    DEPLOY = "deploy"


def build_kind(kind: str | None = None) -> str:
    """
    Build task kind.

    Parameters
    ----------
    kind : str
        Kind to check. If None, return default kind.

    Returns
    -------
    str
        Task kind.
    """
    return kind_builder(TaskKinds, TaskKinds.JOB.value, kind)
