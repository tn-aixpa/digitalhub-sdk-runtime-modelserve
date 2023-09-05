"""
Base Runtime module.
"""
from __future__ import annotations

import typing
from abc import abstractmethod

if typing.TYPE_CHECKING:
    from sdk.entities.function.spec.base import FunctionSpec
    from sdk.entities.task.spec.base import TaskSpec
    from sdk.entities.run.spec.base import RunSpec


class BaseRuntime:
    """
    Base Runtime class.
    """

    def __init__(
        self, function_spec: FunctionSpec, task_spec: TaskSpec, run_spec: RunSpec
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        function_spec : FunctionSpec
            The function specification.
        task_spec : TaskSpec
            The task specification.
        run_spec : RunSpec
            The run specification.
        """
        self.function_spec = function_spec
        self.task_spec = task_spec
        self.run_spec = run_spec

        self.execution_parameters = {}

        if self.run_spec.local_execution:
            self.merge_parameters()

    def merge_parameters(self) -> None:
        """
        Merge the parameters of function, task and run.

        Returns
        -------
        None
        """
        self.execution_parameters = {
            **self.function_spec.to_dict(),
            **self.task_spec.to_dict(),
            **self.run_spec.to_dict(),
        }

    @abstractmethod
    def get_enviroment(self) -> None:
        ...

    @abstractmethod
    def parse_inputs(self, inputs: dict) -> None:
        ...

    @abstractmethod
    def parse_outputs(self, outputs: dict) -> None:
        ...

    @abstractmethod
    def parse_parameters(self, parameters: dict) -> None:
        ...

    @abstractmethod
    def set_enviroment(self, environment: dict) -> None:
        ...

    @abstractmethod
    def execute(self, inputs: dict, parameters: dict) -> None:
        ...

    @abstractmethod
    def parse_results(self, results: dict) -> None:
        ...

    @abstractmethod
    def persist_results(self, outputs: dict) -> None:
        ...
