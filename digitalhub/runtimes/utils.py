from __future__ import annotations

import typing

from digitalhub.factory.factory import factory

if typing.TYPE_CHECKING:
    from digitalhub.runtimes.kind_registry import KindRegistry


def get_kind_registry(kind: str, project: str) -> KindRegistry:
    """
    Get kind registry.

    Parameters
    ----------
    kind : str
        Kind of the runtime.
    project : str
        Project name.

    Returns
    -------
    KindRegistry
        Kind registry.
    """
    runtime = factory.build_runtime(kind, project)
    return runtime.kind_registry
