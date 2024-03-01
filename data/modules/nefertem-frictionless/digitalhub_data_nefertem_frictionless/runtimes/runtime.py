"""
Runtime nefertem module.
"""
from __future__ import annotations

import shutil
import typing
from pathlib import Path
from typing import Callable

from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.generic_utils import build_uuid
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data_nefertem_frictionless.utils.configurations import (
    create_client,
    create_nt_resources,
    create_nt_run_config,
)
from digitalhub_data_nefertem_frictionless.utils.functions import infer, profile, validate
from digitalhub_data_nefertem_frictionless.utils.inputs import get_dataitem_, persist_dataitem
from digitalhub_data_nefertem_frictionless.utils.outputs import build_status, create_artifact, upload_artifact

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact


class RuntimeNefertemFrictionless(Runtime):
    """
    Runtime nefertem class.
    """

    allowed_actions = ["validate", "profile", "infer", "metric"]

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()

        self.output_path = "./nefertem_run"
        self.store = {"name": "local", "store_type": "local"}
        self.nt_id = build_uuid()

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

        Parameters
        ----------
        run : dict
            The run.

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

        LOGGER.info("Collecting inputs.")
        inputs = self._collect_inputs(spec, project)

        LOGGER.info("Configure execution.")
        config = self._configure_execution(inputs, spec, action)

        LOGGER.info("Executing run.")
        results: dict = self._execute(executable, **config)

        LOGGER.info("Collecting outputs.")
        outputs = self._collect_outputs(results, project)
        status = build_status(results, outputs)

        LOGGER.info("Clean up environment.")
        self._cleanup()

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
        if action == "validate":
            return validate
        if action == "profile":
            return profile
        if action == "infer":
            return infer
        raise NotImplementedError

    ####################
    # Inputs
    ####################

    def _collect_inputs(self, spec: dict, project: str) -> list[dict]:
        """
        Collect dataitems inputs.

        Parameters
        ----------
        spec : dict
            Run spec.
        project : str
            The project name.

        Returns
        -------
        list[dict]
            The list of inputs dataitems.
        """
        Path(f"{self.output_path}/tmp").mkdir(parents=True, exist_ok=True)

        mapper = []
        for name in spec.get("inputs", {}).get("dataitems", []):
            dataitem = get_dataitem_(name, project)
            mapper.append(persist_dataitem(dataitem, name, self.output_path))
        return mapper

    ####################
    # Configuration
    ####################

    def _configure_execution(self, inputs: list[dict], spec: dict, action: str) -> tuple[Callable, dict]:
        """
        Generate nefertem configuration.

        Parameters
        ----------
        inputs : list
            The list of inputs dataitems.
        spec : dict
            Run spec.
        action : str
            Action to execute.

        Returns
        -------
        tuple
            Function to execute and its parameters.
        """
        # Create resources
        resources = create_nt_resources(inputs, self.store)

        # Task spec
        task_spec = spec.get(f"{action}_spec")
        framework = task_spec.get("framework")
        parallel = task_spec.get("parallel")
        num_worker = task_spec.get("num_worker")
        exec_args = None
        if action != "validate":
            resource_title = task_spec.get("resource_title")
            resource_description = task_spec.get("resource_description")
            exec_args = {
                "title": resource_title,
                "description": resource_description,
            }

        # Function spec
        function_spec = spec.get("function_spec")
        metrics = function_spec.get("metrics")
        constraints = function_spec.get("constraints")
        error_report = function_spec.get("error_report")

        # Create run configuration
        run_config = create_nt_run_config(action, framework, exec_args, parallel, num_worker)

        # Create Nefertem client
        client = create_client(self.output_path, self.store)

        # Return parameters
        return {
            "client": client,
            "resources": resources,
            "run_config": run_config,
            "run_id": self.nt_id,
            "metrics": metrics,
            "constraints": constraints,
            "error_report": error_report,
        }

    ####################
    # Outputs
    ####################

    def _collect_outputs(self, results: dict, project: str) -> list[Artifact]:
        """
        Collect outputs.

        Parameters
        ----------
        results : dict
            The nefertem run results.
        project : str
            The project name.

        Returns
        -------
        list
            List of artifacts paths.
        """
        output_files = results.get("output_files", [])

        LOGGER.info("Creating artifacts.")
        artifacts = [create_artifact(i, project, self.nt_id) for i in output_files]

        LOGGER.info("Uploading artifacts to minio.")
        for i in artifacts:
            upload_artifact(*i)

        return artifacts

    ####################
    # Cleanup
    ####################

    def _cleanup(self) -> None:
        """
        Cleanup after run.

        Returns
        -------
        None
        """
        shutil.rmtree(f"{self.output_path}/tmp", ignore_errors=True)
