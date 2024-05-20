"""
Runtime class for running Python functions.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable

from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.logger import LOGGER
from digitalhub_ml_python.utils.configuration import get_function_from_source
from digitalhub_ml_python.utils.functions import run_python_job, run_python_nuclio
from digitalhub_ml_python.utils.outputs import build_status


class RuntimePython(Runtime):
    """
    Runtime Python class.
    """

    allowed_actions = ["job", "nuclio"]

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()
        self.root = Path("digitalhub_ml_python")

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
        LOGGER.info("Validating task.")
        action = self._validate_task(run)
        executable = self._get_executable(action)

        LOGGER.info("Starting task.")
        spec = run.get("spec")
        project = run.get("project")

        LOGGER.info("Configuring execution.")
        func = self._configure_execution(spec)

        LOGGER.info("Executing run.")
        results = self._execute(executable, func, project)

        LOGGER.info("Collecting outputs.")
        status = build_status(results)

        # Return run status
        LOGGER.info("Task completed, returning run status.")
        return status

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
        if action == "job":
            return run_python_job
        if action == "nuclio":
            return run_python_nuclio
        raise NotImplementedError

    ####################
    # Configuration
    ####################

    def _configure_execution(self, spec: dict) -> Callable:
        """
        Configure execution.

        Parameters
        ----------
        spec : dict
            Run spec.

        Returns
        -------
        Callable
            Function to execute.
        """
        return get_function_from_source(self.root, spec.get("function_spec"))
