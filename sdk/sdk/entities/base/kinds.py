"""
Kinds builder module.
"""
from __future__ import annotations

import typing

from sdk.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from enum import Enum


def kind_builder(kinds_enum: Enum, default_value: str, kind: str | None = None) -> str:
    """
    Build kind for entities.

    Parameters
    ----------
    kinds_enum : Enum
        Enum class to check.
    default_value : str
        Default kind value.
    kind : str
        Kind to check. If None, return default kind.

    Returns
    -------
    str
        Entity kind.

    Raises
    ------
    EntityError
        If kind is not valid.
    """
    if kind is None:
        return default_value
    values = [item.value for item in kinds_enum]
    if kind not in values:
        raise EntityError(f"Invalid kind '{kind}' for object.")
    return kind
