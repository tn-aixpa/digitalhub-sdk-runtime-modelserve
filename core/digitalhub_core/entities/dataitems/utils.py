"""
Dataitems utils module.
"""
from __future__ import annotations

import typing

from digitalhub_core.utils.commons import DTIT

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.dataitems.entity import Dataitem


def get_dataitem_info(dataitem: Dataitem) -> dict:
    """
    Get the information of an dataitem.

    Parameters
    ----------
    dataitem : Dataitem
        The dataitem.

    Returns
    -------
    dict
        The information of the dataitem.
    """
    return {
        "id": f"store://{dataitem.project}/{DTIT}/{dataitem.kind}/{dataitem.name}:{dataitem.id}",
        "key": dataitem.name,
        "kind": dataitem.kind,
    }
