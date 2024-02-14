"""
Runtime class for running MLRun functions.
"""
from __future__ import annotations

import typing
from typing import Callable

from digitalhub_core.runtimes.base import Runtime
from digitalhub_data.runtimes.results import RunResultsData

if typing.TYPE_CHECKING:
    pass


class RuntimeMLRun(Runtime):
    """
    Runtime MLRun class.
    """

    allowed_actions = ["job", "deploy", "serve"]

    def build(self, function: dict, task: dict, run: dict) -> dict:
        """
        Build run spec.

        Parameters
        ----------
        function : dict
            The function.
        task : dict
            The task.
        run : dict
            The run.

        Returns
        -------
        dict
            The run spec.
        """
        task_kind = task.get("kind").split("+")[1]
        return {
            "function_spec": function.get("spec", {}),
            f"{task_kind}_spec": task.get("spec", {}),
            **run.get("spec", {}),
        }

    def run(self, run: dict) -> dict:
        """
        Run function.

        Returns
        -------
        dict
            Status of the executed run.
        """
        raise RuntimeError("Cannot excute locally.")

    @staticmethod
    def _get_executable(action: str) -> Callable:
        """
        Select function according to action.

        Parameters
        ----------
        action : str
            Action to execute.

        Returns
        -------
        Callable
            Function to execute.
        """
        raise NotImplementedError

    @staticmethod
    def results(run_status: dict) -> RunResultsData:
        """
        Get run results.

        Returns
        -------
        RunResults
            Run results.
        """
        raise NotImplementedError
