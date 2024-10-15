from __future__ import annotations

from digitalhub.entities._base.spec.base import Spec, SpecValidator
from digitalhub.entities.task.models import K8s


class TaskSpec(Spec):
    """Task specification."""

    def __init__(self, function: str) -> None:
        self.function = function


class TaskSpecK8s(TaskSpec):
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
        **kwargs,
    ) -> None:
        super().__init__(function)
        self.node_selector = node_selector
        self.volumes = volumes
        self.resources = resources
        self.affinity = affinity
        self.tolerations = tolerations
        self.envs = envs
        self.secrets = secrets
        self.profile = profile


class TaskValidator(SpecValidator):
    """
    Base task model.
    """

    function: str
    """Function string."""


class TaskValidatorK8s(TaskValidator, K8s):
    """
    Kubernetes task model.
    """
