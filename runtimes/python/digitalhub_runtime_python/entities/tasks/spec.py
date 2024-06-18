"""
Task Python specification module.
"""
from __future__ import annotations

from digitalhub_core.entities.tasks.spec import TaskParamsK8s, TaskSpecK8s
from digitalhub_runtime_python.entities.tasks.models import ContextRef, ContextSource


class TaskSpecJob(TaskSpecK8s):
    """Task Job specification."""

    def __init__(
        self,
        function: str,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function, **kwargs)

        self.backoff_limit = kwargs.get("backoff_limit")
        self.schedule = kwargs.get("schedule")


class TaskParamsJob(TaskParamsK8s):
    """
    TaskParamsJob model.
    """


class TaskSpecBuild(TaskSpecK8s):
    """Task Build specification."""

    def __init__(
        self,
        function: str,
        context_refs: list | None = None,
        context_sources: list | None = None,
        instructions: list | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function, **kwargs)

        self.context_refs = context_refs
        self.context_sources = context_sources
        self.instructions = instructions


class TaskParamsBuild(TaskParamsK8s):
    """
    TaskParamsBuild model.
    """

    context_refs: list[ContextRef] = None
    """Context references."""

    context_sources: list[ContextSource] = None
    """Context sources."""

    instructions: list[str] = None
    """Build instructions."""


class TaskSpecServe(TaskSpecK8s):
    """Task Serve specification."""


class TaskParamsServe(TaskParamsK8s):
    """
    TaskParamsServe model.
    """
