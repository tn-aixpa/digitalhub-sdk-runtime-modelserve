"""
Base Runtime module.
"""
from __future__ import annotations

from abc import abstractmethod


class Runtime:
    """
    Base Runtime class.
    """

    @abstractmethod
    def build(self, function: dict, task: dict, run: dict) -> dict:
        """
        Build run spec.
        """

    @abstractmethod
    def run(self, run: dict) -> dict:
        """
        Execute run task.
        """

    @staticmethod
    def _get_action(run: dict) -> str:
        """
        Get action from run.
        """
        return run.get("spec").get("task").split(":")[0].split("+")[1]
