"""
Runtime class for running MLRun functions.
"""
from __future__ import annotations

import typing
from pathlib import Path
from typing import Callable

from digitalhub_core.entities.artifacts.crud import get_artifact_from_key
from digitalhub_core.entities.dataitems.crud import get_dataitem_from_key
from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data.runtimes.results import RunResultsData
from digitalhub_ml_mlrun.utils.configurations import (
    get_dhcore_function,
    get_mlrun_function,
    get_mlrun_project,
    parse_function_specs,
    save_function_source,
)
from digitalhub_ml_mlrun.utils.functions import run_job
from digitalhub_ml_mlrun.utils.outputs import build_status, parse_mlrun_artifacts

if typing.TYPE_CHECKING:
    from mlrun.runtimes import BaseRuntime
    from mlrun.runtimes.base import RunObject


class RuntimeMLRun(Runtime):
    """
    Runtime MLRun class.
    """

    allowed_actions = ["mlrun"]

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.root_path = Path("/tmp/mlrun_run")
        self.function_source = None

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
        Run function.

        Returns
        -------
        dict
            Status of the executed run.
        """
        LOGGER.info("Validating task.")
        action = self._validate_task(run)
        func = self._get_function(action)

        LOGGER.info("Starting task.")
        spec = run.get("spec")
        project = run.get("project")

        LOGGER.info("Configure execution.")
        mlrun_function, function_args = self._configure_execution(spec, project)

        LOGGER.info("Executing function.")
        results: RunObject = self._execute(func, mlrun_function, function_args)

        LOGGER.info("Collecting results.")
        return self._collect_outputs(results)

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
        if action == "mlrun":
            return run_job
        raise NotImplementedError

    @staticmethod
    def results(run_status: dict) -> RunResultsData:
        """
        Get run results.

        Returns
        -------
        RunResults
            Run results.
        """
        artifacts = run_status.get("artifacts", [])
        artifact_objs = [get_artifact_from_key(art.get("id")) for art in artifacts]
        datatatems = run_status.get("dataitems", [])
        dataitem_objs = [get_dataitem_from_key(dti.get("id")) for dti in datatatems]
        return RunResultsData(artifact_objs, dataitem_objs)

    ####################
    # Configuration
    ####################

    def _configure_execution(self, spec: dict, project: str) -> tuple[BaseRuntime, dict]:
        """
        Create MLRun project and function and prepare parameters.

        Parameters
        ----------
        spec : dict
            Run specs.
        project : str
            Name of the project.

        Returns
        -------
        tuple
            MLRun function and parameters.
        """

        # Setup function source and specs
        LOGGER.info("Getting function source and specs.")
        dhcore_function = get_dhcore_function(spec.get("function"))
        function_source = save_function_source(self.root_path, dhcore_function.spec)
        function_specs = parse_function_specs(dhcore_function.spec)

        # Create MLRun project
        LOGGER.info("Creating MLRun project and function.")
        mlrun_project = get_mlrun_project(project)
        mlrun_function = get_mlrun_function(mlrun_project, dhcore_function.name, function_source, function_specs)

        # Get parameters
        LOGGER.info("Getting parameters.")
        function_args = spec.get("parameters", {})

        return mlrun_function, function_args

    ####################
    # Outputs
    ####################

    def _collect_outputs(self, results: RunObject) -> dict:
        """
        Collect outputs.

        Parameters
        ----------
        results : RunObject
            Execution results.

        Returns
        -------
        dict
            Status of the executed run.
        """
        outputs = parse_mlrun_artifacts(results.status.artifacts)
        return build_status(results, outputs)
