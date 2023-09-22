"""
Runtime build module.
"""
from __future__ import annotations

import typing
from abc import abstractmethod

from sdk.runtimes.objects.base import Runtime

if typing.TYPE_CHECKING:
    from sdk.entities.run.entity import Run


class RuntimeBuild(Runtime):
    """
    Base Runtime build class.
    """

    def __init__(self, spec: dict, run_id: str, project_name: str) -> None:
        """
        Constructor.

        Parameters
        ----------
        spec : dict
            Run merged specification.
        run_id : str
            The run id.
        project_name : str
            The project name.
        """
        self.spec = spec
        self.run_id = run_id
        self.project_name = project_name

    def run(self) -> Run:
        """
        Run the build.

        Returns
        -------
        Run
            The run object.
        """
        return self.build()

    @abstractmethod
    def build(self) -> Run:
        ...
