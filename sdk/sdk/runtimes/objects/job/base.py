"""
Runtime Perform module.
"""
from __future__ import annotations

import typing
from abc import abstractmethod

from sdk.runtimes.objects.base import Runtime

if typing.TYPE_CHECKING:
    from sdk.entities.run.entity import Run


class RuntimeJob(Runtime):
    """
    Base Runtime job class.
    """

    def __init__(self, run: Run) -> None:
        """
        Constructor.

        Parameters
        ----------
        run: Run
            Run object.
        """
        self.spec = run.spec
        self.run_id = run.id
        self.project_name = run.project

    def run(self) -> Run:
        """
        Run the job.

        Returns
        -------
        Run
            The run object.
        """
        return self.job()

    @abstractmethod
    def job(self) -> Run:
        ...
