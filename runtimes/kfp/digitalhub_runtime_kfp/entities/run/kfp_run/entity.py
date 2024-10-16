from __future__ import annotations

import typing

from digitalhub.entities.run._base.entity import Run

if typing.TYPE_CHECKING:
    from digitalhub_runtime_kfp.entities.run.kfp_run.spec import RunSpecKfpRun
    from digitalhub_runtime_kfp.entities.run.kfp_run.status import RunStatusKfpRun

    from digitalhub.entities._base.entity.metadata import Metadata


class RunKfpRun(Run):
    """
    RunKfpRun class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecKfpRun,
        status: RunStatusKfpRun,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecKfpRun
        self.status: RunStatusKfpRun
