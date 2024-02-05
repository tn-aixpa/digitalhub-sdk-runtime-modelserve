"""
Task MLRun specification module.
"""
from __future__ import annotations

from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec


class TaskSpecMLRun(TaskSpec):
    """Task MLRun specification."""


class TaskParamsMLRun(TaskParams):
    """
    TaskParamsMLRun model.
    """


spec_registry = {
    "mlrun": [TaskSpecMLRun, TaskParamsMLRun],
}
