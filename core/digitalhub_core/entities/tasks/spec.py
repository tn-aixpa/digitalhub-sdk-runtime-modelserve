"""
Task specification module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.spec import Spec
from pydantic import BaseModel


class TaskSpec(Spec):
    """Task specification."""

    def __init__(
        self,
        function: str,
        volumes: list[dict] | None = None,
        volume_mounts: list[dict] | None = None,
        env: list[dict] | None = None,
        resources: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        function : str
            The function string of the task.
        volumes : list[dict]
            The volumes of the task.
        volume_mounts : list[dict]
            The volume mounts of the task.
        env : list[dict]
            The env variables of the task.
        resources : dict
            Kubernetes resources for the task.
        """
        self.function = function
        self.volumes = volumes if volumes is not None else []
        self.volume_mounts = volume_mounts if volume_mounts is not None else []
        self.env = env if env is not None else []
        self.resources = resources if resources is not None else {}

        self._any_setter(**kwargs)


class TaskParams(BaseModel):
    """
    Base task model.
    """

    function: str = None
    """Task function."""

    volumes: list[dict] = None
    """Volumes."""

    volume_mounts: list[dict] = None
    """Volume mounts."""

    env: list[dict] = None
    """Env variables."""

    resources: dict = None
    """Resources restrictions."""
