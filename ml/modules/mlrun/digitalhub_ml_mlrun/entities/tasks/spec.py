"""
Task Mlrun specification module.
"""
from __future__ import annotations

from digitalhub_core.entities.tasks.models import K8s
from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec


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


class TaskParamsJob(TaskParams):
    """
    TaskParamsJob model.
    """

    k8s: K8s = None
    """Kubernetes resources."""
