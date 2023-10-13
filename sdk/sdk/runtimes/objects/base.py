"""
Base Runtime module.
"""
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
