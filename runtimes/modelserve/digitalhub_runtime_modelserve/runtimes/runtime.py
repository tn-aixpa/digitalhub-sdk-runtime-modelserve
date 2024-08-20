from __future__ import annotations

import typing
from typing import Callable

from digitalhub_core.context.builder import get_context
from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.logger import LOGGER

if typing.TYPE_CHECKING:
    from digitalhub_core.runtimes.kind_registry import KindRegistry


class RuntimeModelserve(Runtime):
    """
    Runtime Model Serve base class.
    """

    def __init__(self, kind_registry: KindRegistry, project: str) -> None:
        super().__init__(kind_registry, project)
        ctx = get_context(self.project)
        self.root = ctx.runtime_dir
        self.tmp_dir = ctx.tmp_dir

        self.root.mkdir(parents=True, exist_ok=True)
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

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
        msg = f"Local execution not allowed."
        LOGGER.exception(msg)
        raise NotImplementedError(msg)

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
        

class RuntimeSklearnserve(RuntimeModelserve):
    """
    Runtime Sklearn Serve class.
    """

class RuntimeMlflowserve(RuntimeModelserve):
    """
    Runtime Mlflow Serve class.
    """

class RuntimeHuggingfaceserve(RuntimeModelserve):
    """
    Runtime Huggingface Serve class.
    """