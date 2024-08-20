from __future__ import annotations

from digitalhub_core.entities.task.status import TaskStatus

class TaskStatusServe(TaskStatus):
    """
    Task Serve status.
    """

class TaskStatusSklearnserve(TaskStatusServe):
    """
    Task SKLearn Model serve status.
    """

class TaskStatusMlflowserve(TaskStatusServe):
    """
    Task Mlflow Model serve status.
    """

class TaskStatusHuggingfaceserve(TaskStatusServe):
    """
    Task HuggingFace Model serve status.
    """