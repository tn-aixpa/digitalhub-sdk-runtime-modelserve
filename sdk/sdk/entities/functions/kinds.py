"""
Function kind enum module.
"""
from enum import Enum


class FunctionKinds(Enum):
    """
    Function kind enum class.
    """

    MLRUN = "mlrun"
    DBT = "dbt"
    NEFERTEM = "nefertem"
