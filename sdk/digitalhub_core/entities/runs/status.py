"""
RunStatus class module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.status import Status


class RunStatus(Status):
    """
    Status class for run entities.
    """

    def __init__(
        self,
        state: str | None = None,
        dataitems: list | None = None,
        artifacts: list | None = None,
        timing: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        dataitems : list
            Dataitems infos.
        artifacts : list
            Artifacts infos.
        timings : dict
            Run execution times.
        **kwargs
            Keyword arguments.


        See Also
        --------
        Status.__init__
        """
        super().__init__(state, **kwargs)
        self.dataitems = dataitems
        self.artifacts = artifacts
        self.timing = timing
