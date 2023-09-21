"""
Base Runtime module.
"""
from __future__ import annotations

import typing
from abc import abstractmethod

if typing.TYPE_CHECKING:
    from sdk.entities.run.entity import Run


class Runtime:
    """
    Base Runtime class.
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

    @abstractmethod
    def run(self) -> Run:
        ...

    #############################
    # Parse inputs and outputs
    #############################

    @abstractmethod
    def parse_inputs(self) -> None:
        ...

    @abstractmethod
    def parse_outputs(self) -> None:
        ...

    #############################
    # Setup environment
    #############################

    @abstractmethod
    def setup(self) -> None:
        ...

    #############################
    # Execute function
    #############################

    @abstractmethod
    def execute(self) -> None:
        ...

    #############################
    # Parse results
    #############################

    @abstractmethod
    def parse_results(self) -> None:
        ...
