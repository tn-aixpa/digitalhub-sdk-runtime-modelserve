"""
Project kind enum module.
"""
from enum import Enum

from sdk.entities.base.kinds import kind_builder


class ProjectKinds(Enum):
    """
    Project kind enum class.
    """

    PROJECT = "project"


def build_kind(kind: str | None = None) -> str:
    """
    Build project kind.

    Parameters
    ----------
    kind : str
        Kind to check. If None, return default kind.

    Returns
    -------
    str
        Project kind.
    """
    return kind_builder(ProjectKinds, ProjectKinds.PROJECT.value, kind)
