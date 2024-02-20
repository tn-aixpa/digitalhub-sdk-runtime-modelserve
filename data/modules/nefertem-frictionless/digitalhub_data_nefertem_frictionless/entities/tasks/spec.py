"""
Task Dbt specification module.
"""
from __future__ import annotations

import typing
from typing import Optional

from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec
from digitalhub_core.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.tasks.models import Affinity, Env, Label, NodeSelector, Resource, Toleration, Volume


class TaskSpecNefertem(TaskSpec):
    """Task Nefertem specification."""

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
        framework: str | None = None,
        parallel: bool = False,
        num_worker: int | None = 1,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(
            function, node_selector, volumes, resources, labels, affinity, tolerations, env, secrets, **kwargs
        )
        if framework is None:
            raise EntityError("Framework for Nefertem is not given.")
        self.framework = framework
        self.parallel = parallel
        self.num_worker = num_worker


class TaskParamsNefertem(TaskParams):
    """
    TaskParamsNefertem model.
    """

    framework: str = None
    """Nefertem framework."""

    parallel: bool = False
    """Nefertem parallel execution."""

    num_worker: Optional[int] = 1
    """Nefertem number of workers."""


###########################
# Inference
###########################


class TaskSpecInfer(TaskSpecNefertem):
    """Task Infer specification."""

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
        framework: str | None = None,
        parallel: bool = False,
        num_worker: int | None = 1,
        resource_title: str = None,
        resource_description: str = None,
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
            framework,
            parallel,
            num_worker,
            **kwargs,
        )
        self.resource_title = resource_title
        self.resource_description = resource_description


class TaskParamsInfer(TaskParamsNefertem):
    """
    TaskParamsInfer model.
    """

    resource_title: str = None
    """Resource title."""

    resource_description: str = None
    """Resource description."""


###########################
# Profiling
###########################


class TaskSpecProfile(TaskSpecNefertem):
    """Task Profile specification."""

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
        framework: str | None = None,
        parallel: bool = False,
        num_worker: int | None = 1,
        resource_title: str = None,
        resource_description: str = None,
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
            framework,
            parallel,
            num_worker,
            **kwargs,
        )
        self.resource_title = resource_title
        self.resource_description = resource_description


class TaskParamsProfile(TaskParamsNefertem):
    """
    TaskParamsProfile model.
    """

    resource_title: str = None
    """Resource title."""

    resource_description: str = None
    """Resource description."""


###########################
# Validation
###########################


class TaskSpecValidate(TaskSpecNefertem):
    """Task Validate specification."""


class TaskParamsValidate(TaskParamsNefertem):
    """
    TaskParamsValidate model.
    """
