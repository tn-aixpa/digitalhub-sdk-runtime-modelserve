from __future__ import annotations

import shutil
from pathlib import Path
from typing import Callable

from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.logger import LOGGER
from digitalhub_runtime_kfp.utils.configurations import (
    get_dhcore_workflow,
    get_kfp_pipeline,
    parse_workflow_specs,
    save_workflow_source,
)
from digitalhub_runtime_kfp.utils.functions import build_kfp_pipeline, run_kfp_pipeline
from digitalhub_runtime_kfp.utils.inputs import get_inputs_parameters


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

    def build(self, workflow: dict, task: dict, run: dict) -> dict:
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
            "workflow_spec": workflow.get("spec", {}),
            f"{task_kind}_spec": task.get("spec", {}),
            **run.get("spec", {}),
        }

        if task_kind == "pipeline":
            kfp_workflow = self._configure_execution(res, task_kind, run.get("project"))
            pipeline_spec = build_kfp_pipeline(run, kfp_workflow)
            res[f"{task_kind}_spec"]["workflow"] = pipeline_spec
        return res

    def run(self, run: dict) -> dict:
        """
        Run workflow.

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
        workflow_args = self._collect_inputs(spec, self.root_path)

        project = run.get("project")
        LOGGER.info("Configure execution.")
        kfp_workflow = self._configure_execution(spec, action, project)

        LOGGER.info("Executing workflow.")
        results = self._execute(executable, kfp_workflow, workflow_args)

        LOGGER.info("Collecting outputs.")
        status = self._collect_outputs(results, spec)

        LOGGER.info("Cleanup")
        self._cleanup()

        LOGGER.info("Task completed, returning run status.")
        return status

    @staticmethod
    def _get_executable(action: str, run: dict) -> Callable:
        """
        Select workflow according to action.

        Parameters
        ----------
        action : str
            Action to execute.

        Returns
        -------
        Callable
            Workflow to execute.
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
        LOGGER.info("Getting workflow source and specs.")
        dhcore_workflow = get_dhcore_workflow(spec.get(f"{action}_spec", {}).get("function"))
        workflow_source = save_workflow_source(self.root_path, dhcore_workflow.spec.to_dict().get("source"))
        workflow_specs = parse_workflow_specs(dhcore_workflow.spec)

        # Create Mlrun project
        LOGGER.info("Creating KFP project and workflow.")
        return get_kfp_pipeline(dhcore_workflow.name, workflow_source, workflow_specs)

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
