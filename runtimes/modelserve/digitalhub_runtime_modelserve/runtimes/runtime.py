from __future__ import annotations

import typing
from typing import Callable

from digitalhub_core.context.builder import get_context
from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.logger import LOGGER
from digitalhub_runtime_modelserve.utils.function import get_serve_function
from digitalhub_runtime_modelserve.utils.inputs import get_model_files
from digitalhub_runtime_modelserve.utils.configuration import get_function_args

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
        LOGGER.info("Validating task.")
        action = self._validate_task(run)
        executable = self._get_executable(action)

        LOGGER.info("Starting task.")
        spec = run.get("spec")
        project = run.get("project")

        LOGGER.info("Collecting model's files.")
        model_path = self._get_model(spec.get("model_key"), project)

        LOGGER.info("Configure execution.")
        exec_args = self._configure_execution(action, spec, model_path)

        LOGGER.info("Serve model.")
        endpoint = self._execute(executable, exec_args)

        LOGGER.info("Task completed, returning run status.")
        return {"endpoint": endpoint}

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
        return get_serve_function(action)

    def _get_model(self, model_key: str, project: str) -> Callable:
        """
        Get model.

        Parameters
        ----------
        model_key : str
            The model key.
        project : str
            The project.

        Returns
        -------
        str
            The model path.
        """
        return get_model_files(model_key, project)

    def _configure_execution(self, action: str, spec: dict, model_path: str) -> dict:
        """
        Configure execution.

        Parameters
        ----------
        action : str
            The action.
        spec : dict
            The run spec.
        model_path : str
            The model path.

        Returns
        -------
        dict
            Serve model function arguments.
        """
        return get_function_args(action, spec, model_path)


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
