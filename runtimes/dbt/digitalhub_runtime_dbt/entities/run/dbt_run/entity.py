from __future__ import annotations

import typing

from digitalhub.entities.run._base.entity import Run

if typing.TYPE_CHECKING:
    from digitalhub_runtime_dbt.entities.run.dbt_run.spec import RunSpecDbtRun
    from digitalhub_runtime_dbt.entities.run.dbt_run.status import RunStatusDbtRun

    from digitalhub.entities._base.entity.metadata import Metadata


class RunDbtRun(Run):
    """
    RunDbtRun class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecDbtRun,
        status: RunStatusDbtRun,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecDbtRun
        self.status: RunStatusDbtRun
