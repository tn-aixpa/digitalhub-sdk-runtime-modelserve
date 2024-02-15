"""
Task Container specification module.
"""
from __future__ import annotations

from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec


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


class TaskParamsServe(TaskParams):
    """
    TaskParamsServe model.
    """
