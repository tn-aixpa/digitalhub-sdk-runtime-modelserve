"""
Runtime factory module.
"""
from __future__ import annotations

import typing

from sdk.entities.task.kinds import TaskKinds
from sdk.runtimes.builder import RuntimeBuilder
from sdk.runtimes.registry import REGISTRY_RUNTIMES_BUILD, REGISTRY_RUNTIMES_PERFORM

if typing.TYPE_CHECKING:
    from sdk.runtimes.objects.perform.base import Runtime


runtime_builder = RuntimeBuilder()


def get_runtime(function_kind: str, task_kind: str, *args, **kwargs) -> Runtime:
    """
    Get runtime instance by framework and operation.

    Parameters
    ----------
    function_kind : str
        Runtime framework.
    task_kind : str
        Operation to execute.
    *args
        Arguments list.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Runtime
        Runtime instance.
    """
    if task_kind == TaskKinds.BUILD.value:
        registry = REGISTRY_RUNTIMES_BUILD
    elif task_kind == TaskKinds.PERFORM.value:
        registry = REGISTRY_RUNTIMES_PERFORM
    return runtime_builder.build(function_kind, task_kind, registry, *args, **kwargs)
