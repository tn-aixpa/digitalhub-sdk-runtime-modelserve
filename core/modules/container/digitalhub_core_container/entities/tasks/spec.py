"""
Task Container specification module.
"""
from __future__ import annotations

from digitalhub_core.entities.tasks.models import Affinity, Env, Label, NodeSelector, Resource, Toleration, Volume
from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec
from digitalhub_core_container.entities.tasks.models import CorePort


class TaskSpecJob(TaskSpec):
    """Task Job specification."""


class TaskParamsJob(TaskParams):
    """
    TaskParamsJob model.
    """


class TaskSpecDeploy(TaskSpec):
    """Task Deploy specification."""


class TaskParamsDeploy(TaskParams):
    """
    TaskParamsDeploy model.
    """


class TaskSpecServe(TaskSpec):
    """Task Serve specification."""

    def __init__(
        self,
        function: str,
        node_selector: list[NodeSelector] | None = None,
        volumes: list[Volume] | None = None,
        resources: list[Resource] | None = None,
        labels: list[Label] | None = None,
        affinity: Affinity | None = None,
        tolerations: list[Toleration] | None = None,
        env: list[Env] | None = None,
        secrets: list[str] | None = None,
        service_ports: list[CorePort] = None,
        service_type: str = None,
        **kwargs,
    ) -> None:
        super().__init__(
            function,
            node_selector,
            volumes,
            resources,
            labels,
            affinity,
            tolerations,
            env,
            secrets,
            **kwargs,
        )
        self.service_ports = service_ports
        self.service_type = service_type


class TaskParamsServe(TaskParams):
    """
    TaskParamsServe model.
    """

    service_ports: list[CorePort] = None
    """Service ports mapper."""

    service_type: str = None
    """Service type."""
