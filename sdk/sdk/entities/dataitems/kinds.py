"""
Dataitem kind enum module.
"""
from enum import Enum


class DataitemKinds(Enum):
    """
    Dataitem kind enum class.
    """

    DATAITEM = "dataitem"
    TABLE = "table"
    DBT = "dbt"
