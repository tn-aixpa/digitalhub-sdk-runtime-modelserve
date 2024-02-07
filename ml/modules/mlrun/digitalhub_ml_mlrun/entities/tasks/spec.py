"""
Task MLRun specification module.
"""
from __future__ import annotations

from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec


class TaskSpecJob(TaskSpec):
    """Task Job specification."""


class TaskParamsJob(TaskParams):
    """
    TaskParamsJob model.
    """


spec_registry = {
    "mlrun+job": [TaskSpecJob, TaskParamsJob],
}
