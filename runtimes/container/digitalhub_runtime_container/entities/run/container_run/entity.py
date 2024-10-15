from __future__ import annotations

import typing

from digitalhub.entities.run._base.entity import Run

if typing.TYPE_CHECKING:
    from digitalhub_runtime_container.entities.run.container_run.spec import RunSpecContainerRun
    from digitalhub_runtime_container.entities.run.container_run.status import RunStatusContainerRun

    from digitalhub.entities._base.entity.metadata import Metadata


class RunContainerRun(Run):
    """
    RunContainerRun class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecContainerRun,
        status: RunStatusContainerRun,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecContainerRun
        self.status: RunStatusContainerRun
