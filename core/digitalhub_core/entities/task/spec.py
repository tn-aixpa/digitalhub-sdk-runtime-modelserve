from __future__ import annotations

from digitalhub_core.entities._base.spec.base import Spec, SpecParams
from digitalhub_core.entities.task.models import K8s


class TaskSpec(Spec):
    """Task specification."""

    def __init__(self, function: str) -> None:
        self.function = function


class TaskSpecK8s(TaskSpec):
    def __init__(
        self,
        function: str,
        **kwargs,
    ) -> None:
        super().__init__(function)
        self.node_selector = kwargs.get("node_selector")
        self.volumes = kwargs.get("volumes")
        self.resources = kwargs.get("resources")
        self.affinity = kwargs.get("affinity")
        self.tolerations = kwargs.get("tolerations")
        self.envs = kwargs.get("envs")
        self.secrets = kwargs.get("secrets")
        self.profile = kwargs.get("profile")


class TaskParams(SpecParams):
    """
    Base task model.
    """

    function: str
    """Function string."""


class TaskParamsK8s(TaskParams, K8s):
    """
    Kubernetes task model.
    """
