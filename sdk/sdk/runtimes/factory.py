"""
Runtime factory module.
"""
from __future__ import annotations

import typing

from sdk.entities.task.kinds import TaskKinds
from sdk.runtimes.builder import RuntimeBuilder
from sdk.runtimes.registry import REGISTRY_RUNTIMES_BUILD, REGISTRY_RUNTIMES_JOB

if typing.TYPE_CHECKING:
    from sdk.runtimes.objects.job.base import Runtime


runtime_builder = RuntimeBuilder()


def get_runtime(run: dict, *args, **kwargs) -> Runtime:
    """
    Get runtime instance by framework and operation.

    Parameters
    ----------
    run: dict
        Run object.
    *args
        Arguments list.
    **kwargs
        Keyword arguments.

    Returns
    -------
    Runtime
        Runtime instance.
    """
    function_kind, task_kind = run.spec.task.split(":")[0].split("+")
    registry = {}
    if task_kind == TaskKinds.BUILD.value:
        registry = REGISTRY_RUNTIMES_BUILD
    elif task_kind == TaskKinds.JOB.value:
        registry = REGISTRY_RUNTIMES_JOB
    return runtime_builder.build(function_kind, task_kind, registry, run)
