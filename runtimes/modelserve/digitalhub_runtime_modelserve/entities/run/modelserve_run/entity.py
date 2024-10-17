from __future__ import annotations

import typing

import requests

from digitalhub.entities.run._base.entity import Run

if typing.TYPE_CHECKING:
    from digitalhub_runtime_modelserve.entities.run.modelserve_run.spec import RunSpecModelserveRun
    from digitalhub_runtime_modelserve.entities.run.modelserve_run.status import RunStatusModelserveRun

    from digitalhub.entities._base.entity.metadata import Metadata


class RunModelserveRun(Run):
    """
    RunModelserveRun class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecModelserveRun,
        status: RunStatusModelserveRun,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecModelserveRun
        self.status: RunStatusModelserveRun

    def invoke(self, **kwargs) -> requests.Response:
        """
        Invoke run.

        Parameters
        ----------
        kwargs
            Keyword arguments to pass to the request.

        Returns
        -------
        requests.Response
            Response from service.
        """
        if not self._context().local and not self.spec.local_execution:
            local = False
        else:
            local = True
        if kwargs is None:
            kwargs = {}
        return self.status.invoke(local, **kwargs)
