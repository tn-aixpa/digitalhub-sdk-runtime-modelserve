"""
Function kind enum module.
"""
from enum import Enum

from sdk.entities.base.kinds import kind_builder


class FunctionKinds(Enum):
    """
    Function kind enum class.
    """

    MLRUN = "job"
    DBT = "dbt"


def build_kind(kind: str | None = None) -> str:
    """
    Build function kind.

    Parameters
    ----------
    kind : str
        Kind to check. If None, return default kind.

    Returns
    -------
    str
        Function kind.
    """
    return kind_builder(FunctionKinds, FunctionKinds.MLRUN.value, kind)
