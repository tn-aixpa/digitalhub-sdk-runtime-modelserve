"""
Task Python specification module.
"""
from __future__ import annotations

from digitalhub_core.entities.tasks.models import K8s
from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec
from digitalhub_runtime_python.entities.tasks.models import ContextRef, ContextSource


class TaskSpecPythonBase(TaskSpec):
    """Task Python specification for Kubernetes."""

    def __init__(
        self,
        function: str,
        k8s: dict | None = None,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function)
        if k8s is None:
            k8s = {}
        k8s = K8s(**k8s).dict(by_alias=True)
        self.node_selector = k8s.get("node_selector")
        self.volumes = k8s.get("volumes")
        self.resources = k8s.get("resources")
        self.affinity = k8s.get("affinity")
        self.tolerations = k8s.get("tolerations")
        self.envs = k8s.get("envs")
        self.secrets = k8s.get("secrets")
        self.backoff_limit = k8s.get("backoff_limit")
        self.schedule = k8s.get("schedule")
        self.replicas = k8s.get("replicas")


class TaskSpecJob(TaskSpecPythonBase):
    """Task Job specification."""

    def __init__(
        self,
        function: str,
        k8s: dict | None = None,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function, k8s)

        self.backoff_limit = k8s.get("backoff_limit")
        self.schedule = k8s.get("schedule")


class TaskParamsJob(TaskParams):
    """
    TaskParamsJob model.
    """

    k8s: K8s = None
    """Kubernetes resources."""


class TaskSpecBuild(TaskSpecPythonBase):
    """Task Build specification."""

    def __init__(
        self,
        function: str,
        k8s: dict | None = None,
        context_refs: list | None = None,
        context_sources: list | None = None,
        instructions: list | None = None,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function, k8s)
        self.context_refs = context_refs
        self.context_sources = context_sources
        self.instructions = instructions


class TaskParamsBuild(TaskParams):
    """
    TaskParamsBuild model.
    """

    k8s: K8s = None
    """Kubernetes resources."""

    context_refs: list[ContextRef] = None
    """Context references."""

    context_sources: list[ContextSource] = None
    """Context sources."""

    instructions: list[str] = None
    """Build instructions."""
