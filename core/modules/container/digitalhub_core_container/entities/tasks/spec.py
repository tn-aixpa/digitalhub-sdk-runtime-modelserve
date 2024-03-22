"""
Task Container specification module.
"""
from __future__ import annotations

from digitalhub_core.entities.tasks.models import K8s
from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec
from digitalhub_core_container.entities.tasks.models import CorePort


class TaskSpecJob(TaskSpec):
    """Task Job specification."""

    def __init__(
        self,
        function: str,
        k8s: K8s | None = None,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function)
        if k8s is None:
            k8s = {}
        k8s = K8s(**k8s)
        self.node_selector = k8s.node_selector
        self.volumes = k8s.volumes
        self.resources = k8s.resources
        self.affinity = k8s.affinity
        self.tolerations = k8s.tolerations
        self.labels = k8s.labels
        self.env = k8s.env
        self.secrets = k8s.secrets
        self.backoff_limit = k8s.backoff_limit
        self.schedule = k8s.schedule
        self.replicas = k8s.replicas


class TaskParamsJob(TaskParams):
    """
    TaskParamsJob model.
    """

    k8s: K8s = None
    """Kubernetes resources."""


class TaskSpecDeploy(TaskSpec):
    """Task Deploy specification."""

    def __init__(
        self,
        function: str,
        k8s: K8s | None = None,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function)
        if k8s is None:
            k8s = {}
        k8s = K8s(**k8s)
        self.node_selector = k8s.node_selector
        self.volumes = k8s.volumes
        self.resources = k8s.resources
        self.affinity = k8s.affinity
        self.tolerations = k8s.tolerations
        self.labels = k8s.labels
        self.env = k8s.env
        self.secrets = k8s.secrets
        self.backoff_limit = k8s.backoff_limit
        self.schedule = k8s.schedule
        self.replicas = k8s.replicas


class TaskParamsDeploy(TaskParams):
    """
    TaskParamsDeploy model.
    """

    k8s: K8s = None
    """Kubernetes resources."""


class TaskSpecServe(TaskSpec):
    """Task Serve specification."""

    def __init__(
        self,
        function: str,
        k8s: K8s | None = None,
        service_ports: list[CorePort] = None,
        service_type: str = None,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function)
        if k8s is None:
            k8s = {}
        k8s = K8s(**k8s)
        self.node_selector = k8s.node_selector
        self.volumes = k8s.volumes
        self.resources = k8s.resources
        self.affinity = k8s.affinity
        self.tolerations = k8s.tolerations
        self.labels = k8s.labels
        self.env = k8s.env
        self.secrets = k8s.secrets
        self.backoff_limit = k8s.backoff_limit
        self.schedule = k8s.schedule
        self.replicas = k8s.replicas
        self.service_ports = service_ports
        self.service_type = service_type


class TaskParamsServe(TaskParams):
    """
    TaskParamsServe model.
    """

    k8s: K8s = None
    """Kubernetes resources."""

    service_ports: list[CorePort] = None
    """Service ports mapper."""

    service_type: str = None
    """Service type."""
