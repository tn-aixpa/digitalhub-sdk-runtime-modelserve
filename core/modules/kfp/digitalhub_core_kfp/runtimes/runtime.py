from __future__ import annotations

import shutil
from pathlib import Path
from typing import Callable

from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.logger import LOGGER
from digitalhub_core_kfp.utils.configurations import (
    get_dhcore_function,
    get_kfp_pipeline,
    parse_function_specs,
    save_function_source,
)
from digitalhub_core_kfp.utils.functions import build_kfp_pipeline, run_kfp_pipeline
from digitalhub_core_kfp.utils.inputs import get_inputs_parameters


class RuntimeKFP(Runtime):
    """
    Runtime KFP class.
    """

    allowed_actions = ["pipeline"]

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()

        self.root_path = Path("/tmp/kfp_run")
        self.function_source = None

        self.root_path.mkdir(parents=True, exist_ok=True)

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
        res = {
            "function_spec": function.get("spec", {}),
            f"{task_kind}_spec": task.get("spec", {}),
            **run.get("spec", {}),
        }

        if task_kind == "pipeline":
            kfp_function = self._configure_execution(res, task_kind, run.get("project"))
            pipeline_spec = build_kfp_pipeline(run, kfp_function)
            res[f"{task_kind}_spec"]["workflow"] = pipeline_spec
        return res

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
        executable = self._get_executable(action, run)

        LOGGER.info("Starting task.")
        spec = run.get("spec")

        LOGGER.info("Collecting inputs.")
        function_args = self._collect_inputs(spec, self.root_path)

        project = run.get("project")
        LOGGER.info("Configure execution.")
        kfp_function = self._configure_execution(spec, action, project)

        LOGGER.info("Executing function.")
        results = self._execute(executable, kfp_function, function_args)

        LOGGER.info("Collecting outputs.")
        status = self._collect_outputs(results, spec)

        LOGGER.info("Cleanup")
        self._cleanup()

        LOGGER.info("Task completed, returning run status.")
        return status

    @staticmethod
    def _get_executable(action: str, run: dict) -> Callable:
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
        if action == "pipeline":
            return run_kfp_pipeline(run)
        raise NotImplementedError

    ####################
    # Helpers
    ####################
    def _collect_inputs(self, spec: dict, tmp_dir: str) -> dict:
        """
        Collect inputs.

        Parameters
        ----------
        spec : dict
            Run specs.
        project : str
            Name of the project.

        Returns
        -------
        dict
            Parameters.
        """
        LOGGER.info("Getting inputs.")
        inputs = spec.get("inputs", {})
        parameters = spec.get("parameters", {})
        return get_inputs_parameters(inputs, parameters)

    ####################
    # Configuration
    ####################

    def _configure_execution(self, spec: dict, action: str, project: str):
        """
        Create KFP pipeline and prepare parameters.

        Parameters
        ----------
        spec : dict
            Run specs.
        action : str
            Action to execute.
        project : str
            Name of the project.

        Returns
        -------
        tuple
            KFP pipeline to execute and parameters.
        """

        # Setup function source and specs
        LOGGER.info("Getting function source and specs.")
        dhcore_function = get_dhcore_function(spec.get(f"{action}_spec", {}).get("function"))
        function_source = save_function_source(self.root_path, dhcore_function.spec)
        function_specs = parse_function_specs(dhcore_function.spec)

        # Create Mlrun project
        LOGGER.info("Creating KFP project and function.")
        return get_kfp_pipeline(dhcore_function.name, function_source, function_specs)

    ####################
    # Outputs
    ####################

    def _collect_outputs(self, results: dict, spec: dict) -> dict:
        """
        Collect outputs. Use the produced results directly

        Parameters
        ----------
        results : RunObject
            Execution results.

        Returns
        -------
        dict
            Status of the executed run.
        """
        return results

    ####################
    # Cleanup
    ####################

    def _cleanup(self) -> None:
        """
        Cleanup root folder.

        Returns
        -------
        None
        """
        shutil.rmtree(self.root_path, ignore_errors=True)
