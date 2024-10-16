from __future__ import annotations

import typing

from digitalhub.entities.run._base.entity import Run

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.run.python_run.spec import RunSpecPythonRun
    from digitalhub_runtime_python.entities.run.python_run.status import RunStatusPythonRun

    from digitalhub.entities._base.entity.metadata import Metadata


class RunPythonRun(Run):
    """
    RunPythonRun class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecPythonRun,
        status: RunStatusPythonRun,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecPythonRun
        self.status: RunStatusPythonRun
