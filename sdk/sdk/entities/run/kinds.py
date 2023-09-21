"""
Run kind enum module.
"""
from enum import Enum

from sdk.entities.base.kinds import kind_builder


class RunKinds(Enum):
    """
    Run kind enum class.
    """

    RUN = "run"


def build_kind(kind: str | None = None) -> str:
    """
    Build run kind.

    Parameters
    ----------
    kind : str
        Kind to check. If None, return default kind.

    Returns
    -------
    str
        Run kind.
    """
    return kind_builder(RunKinds, RunKinds.RUN.value, kind)
