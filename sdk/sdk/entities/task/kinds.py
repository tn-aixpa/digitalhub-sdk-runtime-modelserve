"""
Task kind enum module.
"""
from enum import Enum

from sdk.entities.base.kinds import kind_builder


class TaskKinds(Enum):
    """
    Task kind enum class.
    """

    PERFORM = "perform"
    BUILD = "build"


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
    return kind_builder(TaskKinds, TaskKinds.PERFORM.value, kind)
