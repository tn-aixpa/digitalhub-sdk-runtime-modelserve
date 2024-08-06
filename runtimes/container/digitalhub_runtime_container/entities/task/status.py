from __future__ import annotations

from digitalhub_core.entities.task.status import TaskStatus


class TaskStatusJob(TaskStatus):
    """
    Task Job status.
    """


class TaskStatusDeploy(TaskStatus):
    """
    Task Deploy status.
    """


class TaskStatusServe(TaskStatus):
    """
    Task Serve status.
    """


class TaskStatusBuild(TaskStatus):
    """
    Task Build status.
    """
