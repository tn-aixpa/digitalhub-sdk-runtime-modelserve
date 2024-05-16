"""
Task Python specification module.
"""
from __future__ import annotations

from digitalhub_core.entities.tasks.models import K8s
from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec


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
        self.env = k8s.get("env")
        self.secrets = k8s.get("secrets")
        self.backoff_limit = k8s.get("backoff_limit")
        self.schedule = k8s.get("schedule")
        self.replicas = k8s.get("replicas")


class TaskSpecJob(TaskSpecPythonBase):
    """Task Job specification."""


class TaskParamsJob(TaskParams):
    """
    TaskParamsJob model.
    """

    k8s: K8s = None
    """Kubernetes resources."""


class TaskSpecNuclio(TaskSpecPythonBase):
    """Task Nuclio specification."""


class TaskParamsNuclio(TaskParams):
    """
    TaskParamsNuclio model.
    """

    k8s: K8s = None
    """Kubernetes resources."""
