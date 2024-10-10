from __future__ import annotations

from digitalhub.entities.task.status import TaskStatus


class TaskStatusJob(TaskStatus):
    """
    Task Job status.
    """


class TaskStatusBuild(TaskStatus):
    """
    Task Build status.
    """


class TaskStatusServe(TaskStatus):
    """
    Task Serve status.
    """
