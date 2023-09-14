"""
Runtime factory module.
"""
from __future__ import annotations

import typing

from sdk.runtimes.builder import RuntimeBuilder

if typing.TYPE_CHECKING:
    from sdk.runtimes.objects.base import Runtime


runtime_builder = RuntimeBuilder()


def get_runtime(kind: str, *args, **kwargs) -> Runtime:
    """
    Get runtime instance by kind.

    Parameters
    ----------
    kind : str
        Kind of runtime.
    *args
        Arguments list.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Runtime
        Runtime instance.
    """
    return runtime_builder.build(kind, *args, **kwargs)
