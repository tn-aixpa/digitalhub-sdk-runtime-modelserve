"""
Runtime class for running MLRun functions.
"""
from __future__ import annotations

from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.logger import LOGGER


class RuntimeMLrun(Runtime):
    """
    Runtime Nefertem class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """

    def build(self, function: dict, task: dict, run: dict) -> dict:
        """
        Merge specs.
        """
        return {
            **function.get("spec", {}),
            **task.get("spec", {}),
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
        # Get action
        action = self._get_action(run)

        # Handle unknown task kind
        if action not in ["mlrun"]:
            msg = f"Task {action} not allowed for MLRun runtime"
            LOGGER.error(msg)
            raise EntityError(msg)

        # Execute action
        return self.execute(action, run)

    ####################
    # Execute
    ####################

    def execute(self, action: str, run: dict) -> dict:
        """
        Execute function.

        Returns
        -------
        dict
            Status of the executed run.
        """
