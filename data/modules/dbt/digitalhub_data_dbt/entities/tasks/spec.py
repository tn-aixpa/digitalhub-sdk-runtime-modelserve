"""
Task Transform specification module.
"""
from __future__ import annotations

from digitalhub_core.entities.tasks.spec import TaskParams, TaskSpec


class TaskSpecTransform(TaskSpec):
    """Task Transform specification."""


class TaskParamsTransform(TaskParams):
    """
    TaskParamsTransform model.
    """


spec_registry = {
    "transform": [TaskSpecTransform, TaskParamsTransform],
}
