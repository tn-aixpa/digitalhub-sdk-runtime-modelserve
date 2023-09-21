"""
Dataitem kind enum module.
"""
from enum import Enum

from sdk.entities.base.kinds import kind_builder


class DataitemKinds(Enum):
    """
    Dataitem kind enum class.
    """

    DATAITEM = "dataitem"
    TABLE = "table"
    DBT = "dbt"


def build_kind(kind: str | None = None) -> str:
    """
    Build dataitem kind.

    Parameters
    ----------
    kind : str
        Kind to check. If None, return default kind.

    Returns
    -------
    str
        Dataitem kind.
    """
    return kind_builder(DataitemKinds, DataitemKinds.DATAITEM.value, kind)
