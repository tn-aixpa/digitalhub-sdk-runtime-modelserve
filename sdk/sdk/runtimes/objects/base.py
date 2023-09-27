"""
Base Runtime module.
"""
from abc import abstractmethod


class Runtime:
    """
    Base Runtime class.
    """

    @abstractmethod
    def run(self, run: dict) -> dict:
        # Runner, si occupa di esegure la run
        ...

    @abstractmethod
    def build(self, function: dict, task: dict, run: dict) -> dict:
        # Builder, si occupa di fare merge delle spec
        ...

    @abstractmethod
    def get_allowed_tasks(self) -> list:
        # return list of tasks
        ...
