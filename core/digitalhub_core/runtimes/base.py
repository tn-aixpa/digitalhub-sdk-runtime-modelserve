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
        Get action to execute from run.

        The run object stores in its spec the identifier of the task
        it is associated with. The task string is derived from the
        function string, and has the following format:

        <function-kind>+<task-action>://<function-name>:<function-id>

        Parameters
        ----------
        run : dict
            Run object dictionary.

        Returns
        -------
        str
            Action to execute.

        Raises
        ------
        RuntimeError
            If malformed run spec.

        Examples
        --------
        >>> run = {"spec": {"task": dbt+transform://dbt-example-function:some-uuid4}}
        >>> Runtime._get_action(run)
        'transform'
        """
        try:
            return run["spec"]["task"].split(":")[0].split("+")[1]
        except (KeyError, IndexError):
            raise RuntimeError("Malformed run spec.")
