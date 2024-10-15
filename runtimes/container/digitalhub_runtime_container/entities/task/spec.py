from __future__ import annotations

from digitalhub_runtime_container.entities.task.models import CorePort

from digitalhub.entities.task.spec import TaskSpecK8s, TaskValidatorK8s


class TaskSpecJob(TaskSpecK8s):
    """
    Task Job specifications.
    """

    def __init__(
        self,
        function: str,
        node_selector: dict | None = None,
        volumes: list | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list | None = None,
        envs: list | None = None,
        secrets: list | None = None,
        profile: str | None = None,
        backoff_limit: int | None = None,
        schedule: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            function,
            node_selector,
            volumes,
            resources,
            affinity,
            tolerations,
            envs,
            secrets,
            profile,
            **kwargs,
        )
        self.backoff_limit = backoff_limit
        self.schedule = schedule


class TaskValidatorJob(TaskValidatorK8s):
    """
    TaskValidatorJob model.
    """

    backoff_limit: int = None
    """Backoff limit."""

    schedule: str = None
    """Schedule."""


class TaskSpecDeploy(TaskSpecK8s):
    """
    Task Deploy specifications.
    """

    def __init__(
        self,
        function: str,
        node_selector: dict | None = None,
        volumes: list | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list | None = None,
        envs: list | None = None,
        secrets: list | None = None,
        profile: str | None = None,
        replicas: int | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            function,
            node_selector,
            volumes,
            resources,
            affinity,
            tolerations,
            envs,
            secrets,
            profile,
            **kwargs,
        )
        self.replicas = replicas


class TaskValidatorDeploy(TaskValidatorK8s):
    """
    TaskValidatorDeploy model.
    """

    replicas: int = None
    """Replicas."""


class TaskSpecServe(TaskSpecK8s):
    """
    Task Serve specifications.
    """

    def __init__(
        self,
        function: str,
        node_selector: dict | None = None,
        volumes: list | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list | None = None,
        envs: list | None = None,
        secrets: list | None = None,
        profile: str | None = None,
        replicas: int | None = None,
        service_ports: list | None = None,
        service_type: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            function,
            node_selector,
            volumes,
            resources,
            affinity,
            tolerations,
            envs,
            secrets,
            profile,
            **kwargs,
        )
        self.replicas = replicas
        self.service_ports = service_ports
        self.service_type = service_type


class TaskValidatorServe(TaskValidatorK8s):
    """
    TaskValidatorServe model.
    """

    replicas: int = None
    """Replicas."""

    service_ports: list[CorePort] = None
    """Service ports mapper."""

    service_type: str = None
    """Service type."""


class TaskSpecBuild(TaskSpecK8s):
    """
    Task Build specifications.
    """

    def __init__(
        self,
        function: str,
        node_selector: dict | None = None,
        volumes: list | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list | None = None,
        envs: list | None = None,
        secrets: list | None = None,
        profile: str | None = None,
        instructions: list | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            function,
            node_selector,
            volumes,
            resources,
            affinity,
            tolerations,
            envs,
            secrets,
            profile,
            **kwargs,
        )
        self.instructions = instructions


class TaskValidatorBuild(TaskValidatorK8s):
    """
    TaskValidatorBuild model.
    """

    instructions: list[str] = None
    """Build instructions."""
