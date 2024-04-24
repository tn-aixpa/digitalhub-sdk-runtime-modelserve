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
        k8s: dict | None = None,
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


class TaskSpecBuild(TaskSpec):
    """Task Build specification."""

    def __init__(
        self,
        function: str,
        k8s: dict | None = None,
        target_image: str | None = None,
        commands: list[str] | None = None,
        force_build: bool = False,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(function)
        self.k8s = k8s
        self.target_image = target_image
        self.commands = commands
        self.force_build = force_build

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
        dict_["target_image"] = self.target_image
        dict_["commands"] = self.commands
        dict_["force_build"] = self.force_build
        return dict_


class TaskParamsBuild(TaskParams):
    """
    TaskParamsBuild model.
    """

    k8s: K8s = None
    """Kubernetes resources."""

    target_image: str = None
    """
    Target image.
    """

    commands: list[str] = None
    """
     List of docker build (RUN) commands e.g. ['pip install pandas']
    """

    force_build: bool = False
    """
    Force build even if no changes have been made.
    """
