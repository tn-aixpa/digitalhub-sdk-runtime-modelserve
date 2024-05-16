"""
Runtime class for running Python functions.
"""
from __future__ import annotations

from typing import Callable

from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.logger import LOGGER
from digitalhub_ml_python.utils.functions import run_python_job, run_python_nuclio


class RuntimePython(Runtime):
    """
    Runtime Python class.
    """

    allowed_actions = ["job", "nuclio"]

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
    def _get_executable(action: str, function_spec: dict) -> Callable:
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
        if action == "job":
            return run_python_job
        if action == "nuclio":
            return run_python_nuclio
        raise NotImplementedError
