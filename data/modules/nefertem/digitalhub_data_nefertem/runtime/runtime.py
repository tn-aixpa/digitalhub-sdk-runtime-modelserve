"""
Runtime nefertem module.
"""
from __future__ import annotations

import shutil
import typing
from pathlib import Path
from typing import Callable

from digitalhub_core.entities.artifacts.crud import get_artifact_from_key
from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.runtimes.results import RunResults
from digitalhub_core.utils.generic_utils import build_uuid
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data_nefertem.utils.configurations import create_client, create_nt_resources, create_nt_run_config
from digitalhub_data_nefertem.utils.functions import infer, metric, profile, validate
from digitalhub_data_nefertem.utils.inputs import get_dataitem_, persist_dataitem
from digitalhub_data_nefertem.utils.outputs import build_status, create_artifact, upload_artifact

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact


class RuntimeNefertem(Runtime):
    """
    Runtime nefertem class.
    """

    allowed_actions = ["validate", "profile", "infer", "metric"]

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.output_path = "/tmp/nefertem_run"
        self.store = {"name": "local", "store_type": "local"}
        self.nt_id = build_uuid()

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
        Execute function.

        Returns
        -------
        dict
            Status of the executed run.
        """
        # Validate task
        LOGGER.info("Validating task.")
        action = self._validate_task(run)
        func = self._get_function(action)

        # Get run specs
        LOGGER.info("Starting task.")
        spec = run.get("spec")
        project = run.get("project")

        # Collect inputs
        LOGGER.info("Collecting inputs.")
        inputs = self._collect_inputs(spec.get("inputs", {}).get("dataitems", []), project)

        # Get nefertem configuration and function
        LOGGER.info("Configure execution.")
        config = self._configure_execution(inputs, spec, action)

        # Execute function
        LOGGER.info("Executing run.")
        results: dict = self._execute(func, **config)

        # Collect outputs
        LOGGER.info("Collecting outputs.")
        outputs = self._collect_outputs(results, project, self.nt_id)
        status = build_status(results, outputs)

        # Remove tmp folder
        LOGGER.info("Removing tmp folder.")
        self.cleanup()

        # Return run status
        LOGGER.info("Task completed, returning run status.")
        return status

    @staticmethod
    def _get_function(action: str) -> Callable:
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
        if action == "metric":
            return metric
        raise NotImplementedError

    @staticmethod
    def results(run_status: dict) -> RunResults:
        """
        Get run results.

        Returns
        -------
        RunResults
            Run results.
        """
        artifacts = run_status.get("artifacts", [])
        artifact_objs = [get_artifact_from_key(art.get("id")) for art in artifacts]
        return RunResults(artifact_objs)

    ####################
    # Inputs
    ####################

    def _collect_inputs(self, inputs: list, project: str) -> list[dict]:
        """
        Materialize inputs in postgres.

        Parameters
        ----------
        inputs : list
            The list of inputs dataitems names.
        project : str
            The project name.

        Returns
        -------
        list[dict]
            The list of inputs dataitems.
        """
        Path(f"{self.output_path}/tmp").mkdir(parents=True, exist_ok=True)

        mapper = []
        for name in inputs:
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

        # Create run configuration
        run_config = create_nt_run_config(action, spec)

        # Create Nefertem client
        client = create_client(self.output_path, self.store)

        # Return parameters
        return {
            "client": client,
            "resources": resources,
            "run_config": run_config,
            "run_id": self.nt_id,
            "metrics": spec.get("metrics"),
            "constraints": spec.get("constraints"),
            "error_report": spec.get("error_report"),
        }

    ####################
    # Outputs
    ####################

    def _collect_outputs(self, results: dict, project: str, run_id: str) -> list[Artifact]:
        """
        Collect outputs.

        Parameters
        ----------
        results : dict
            The nefertem run results.
        project : str
            The project name.
        run_id : str
            Neferetem run id.

        Returns
        -------
        list
            List of artifacts paths.
        """
        output_files = results.get("output_files", [])

        LOGGER.info("Creating artifacts.")
        artifacts = [create_artifact(i, project, run_id) for i in output_files]

        LOGGER.info("Uploading artifacts to minio.")
        [upload_artifact(*i) for i in artifacts]

        return artifacts

    ####################
    # Cleanup
    ####################

    def cleanup(self) -> None:
        """
        Cleanup after run.

        Returns
        -------
        None
        """
        shutil.rmtree(f"{self.output_path}/tmp", ignore_errors=True)
