from __future__ import annotations

import typing

from digitalhub_runtime_modelserve.entities.task.modelserve_serve.entity import TaskModelserveServe

if typing.TYPE_CHECKING:
    from digitalhub_runtime_modelserve.entities.task.mlflowserve_serve.spec import TaskSpecMlflowserveServe
    from digitalhub_runtime_modelserve.entities.task.mlflowserve_serve.status import TaskStatusMlflowserveServe

    from digitalhub.entities._base.entity.metadata import Metadata


class TaskModelserveServe(TaskModelserveServe):
    """
    TaskModelserveServe class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: TaskSpecMlflowserveServe,
        status: TaskStatusMlflowserveServe,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: TaskSpecMlflowserveServe
        self.status: TaskStatusMlflowserveServe
