"""
Task DBT specification module.
"""
from __future__ import annotations

import typing
from typing import Optional

from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec
from digitalhub_core.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.tasks.models import Env, NodeSelector, Resource, Volume


class TaskSpecNefertem(TaskSpec):
    """Task Nefertem specification."""

    def __init__(
        self,
        function: str,
        node_selector: NodeSelector | None = None,
        volumes: list[Volume] | None = None,
        resources: Resource | None = None,
        env: list[Env] | None = None,
        framework: str | None = None,
        exec_args: dict | None = None,
        parallel: bool = False,
        num_worker: int | None = 1,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function, node_selector, volumes, resources, env, **kwargs)
        if framework is None:
            raise EntityError("Framework for Nefertem is not given.")
        self.framework = framework
        self.exec_args = exec_args
        self.parallel = parallel
        self.num_worker = num_worker


class TaskParamsNefertem(TaskParams):
    """
    TaskParamsNefertem model.
    """

    framework: str = None
    """Nefertem framework."""

    exec_args: Optional[dict] = {}
    """Nefertem execution arguments."""

    parallel: bool = False
    """Nefertem parallel execution."""

    num_worker: Optional[int] = 1
    """Nefertem number of workers."""


###########################
# Inference
###########################


class TaskSpecInfer(TaskSpecNefertem):
    """Task Infer specification."""


class TaskParamsInfer(TaskParamsNefertem):
    """
    TaskParamsInfer model.
    """


###########################
# Profiling
###########################


class TaskSpecProfile(TaskSpecNefertem):
    """Task Profile specification."""


class TaskParamsProfile(TaskParamsNefertem):
    """
    TaskParamsProfile model.
    """


###########################
# Validation
###########################


class TaskSpecValidate(TaskSpecNefertem):
    """Task Validate specification."""


class TaskParamsValidate(TaskParamsNefertem):
    """
    TaskParamsValidate model.
    """


###########################
# Metric
###########################


class TaskSpecMetric(TaskSpecNefertem):
    """Task Metric specification."""


class TaskParamsMetric(TaskParamsNefertem):
    """
    TaskParamsMetric model.
    """


SPEC_REGISTRY = {
    "infer": [TaskSpecInfer, TaskParamsInfer],
    "profile": [TaskSpecProfile, TaskParamsProfile],
    "validate": [TaskSpecValidate, TaskParamsValidate],
    "metric": [TaskSpecMetric, TaskParamsMetric],
}
