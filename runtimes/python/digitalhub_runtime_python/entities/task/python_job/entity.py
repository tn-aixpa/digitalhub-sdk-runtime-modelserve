from __future__ import annotations

import typing

from digitalhub.entities.task._base.entity import Task

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.task.python_job.spec import TaskSpecPythonJob
    from digitalhub_runtime_python.entities.task.python_job.status import TaskStatusPythonJob

    from digitalhub.entities._base.entity.metadata import Metadata


class TaskPythonJob(Task):
    """
    TaskPythonJob class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: TaskSpecPythonJob,
        status: TaskStatusPythonJob,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: TaskSpecPythonJob
        self.status: TaskStatusPythonJob
