"""
Task Dbt specification module.
"""
from __future__ import annotations

from typing import Optional

from digitalhub_core.entities.tasks.models import K8s
from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec


class TaskSpecNefertem(TaskSpec):
    """Task Nefertem specification."""

    def __init__(
        self,
        function: str,
        framework: str,
        exec_args: dict | None = None,
        parallel: bool = False,
        num_worker: int | None = 1,
        k8s: K8s | None = None,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function)

        self.framework = framework
        self.exec_args = exec_args
        self.parallel = parallel
        self.num_worker = num_worker
        self.k8s = k8s

    def to_dict(self) -> dict:
        """
        Override to_dict to filter k8s None.

        Returns
        -------
        dict
            Dictionary representation of the object.
        """
        dict_ = super().to_dict()
        if self.k8s is not None:
            dict_["k8s"] = {k: v for k, v in dict_["k8s"].items() if v is not None}
        return dict_


class TaskParamsNefertem(TaskParams):
    """
    TaskParamsNefertem model.
    """

    framework: str
    """Nefertem framework."""

    exec_args: Optional[dict] = {}
    """Nefertem execution arguments."""

    parallel: bool = False
    """Nefertem parallel execution."""

    num_worker: Optional[int] = 1
    """Nefertem number of workers."""

    k8s: Optional[K8s] = None
    """Kubernetes resources."""


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
