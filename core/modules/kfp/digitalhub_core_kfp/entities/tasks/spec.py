"""
Task KFP specification module.
"""
from __future__ import annotations

from digitalhub_core.entities.tasks.models import K8s
from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec


class TaskSpecPipeline(TaskSpec):
    """Task Pipeline specification."""

    def __init__(self, function: str, workflow: str | None = None, k8s: K8s | None = None) -> None:
        """
        Constructor.
        """
        super().__init__(function)
        if k8s is None:
            k8s = {}
        k8s = K8s(**k8s).dict(by_alias=True)
        self.env = k8s.get("env")
        self.secrets = k8s.get("secrets")
        self.schedule = k8s.get("schedule")
        self.workflow = workflow

    def to_dict(self) -> dict:
        """
        Override to_dict to filter k8s None.

        Returns
        -------
        dict
            Dictionary representation of the object.
        """
        dict_ = super().to_dict()
        if "k8s" in dict_:
            dict_["k8s"] = {k: v for k, v in dict_["k8s"].items() if v is not None}
        return dict_


class TaskParamsPipeline(TaskParams):
    """
    TaskParamsPipeline model.
    """

    k8s: K8s
    """Kubernetes resources."""

    workflow: str = None
    """KFP workflow specification as YAML string."""