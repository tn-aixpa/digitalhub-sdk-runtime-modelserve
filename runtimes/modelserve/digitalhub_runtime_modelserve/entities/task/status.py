from __future__ import annotations

from digitalhub_core.entities.task.status import TaskStatus


class TaskStatusServe(TaskStatus):
    """
    Task Serve status.
    """


class TaskStatusSklearnserveServe(TaskStatusServe):
    """
    Task SKLearn Model serve status.
    """


class TaskStatusMlflowserveServe(TaskStatusServe):
    """
    Task Mlflow Model serve status.
    """


class TaskStatusHuggingfaceserveServe(TaskStatusServe):
    """
    Task HuggingFace Model serve status.
    """
