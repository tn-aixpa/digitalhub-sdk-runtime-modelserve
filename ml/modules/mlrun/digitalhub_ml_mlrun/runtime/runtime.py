"""
Runtime class for running MLRun functions.
"""
from __future__ import annotations

import typing
from pathlib import Path

import mlrun
from digitalhub_core.entities.functions.crud import get_function
from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import decode_string
from digitalhub_core.utils.logger import LOGGER

if typing.TYPE_CHECKING:
    from mlrun.projects import MlrunProject
    from mlrun.runtimes import BaseRuntime
    from digitalhub_core.entities.functions.entity import Function


class RuntimeMLrun(Runtime):
    """
    Runtime Nefertem class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.root_path = Path("/tmp")
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
        # Get action
        action = self._get_action(run)

        # Handle unknown task kind
        if action not in ["mlrun"]:
            msg = f"Task {action} not allowed for MLRun runtime"
            LOGGER.error(msg)
            raise EntityError(msg)

        # Execute action
        return self.execute(action, run)

    ####################
    # Execute
    ####################

    def execute(self, action: str, run: dict) -> dict:
        """
        Execute function.

        Returns
        -------
        dict
            Status of the executed run.
        """

        # Get run specs
        LOGGER.info("Starting task.")
        spec = run.get("spec")
        project = run.get("project")

        # Setup function source and specs
        LOGGER.info("Getting function source.")
        dhcore_function = self._get_dhcore_function(project, spec)
        function_source = self._save_function_source(dhcore_function)
        function_specs = self._parse_function_specs(dhcore_function)

        # Get parameters
        LOGGER.info("Getting parameters.")
        parameters = {}#spec.get("parameters", {})

        # Create MLRun project
        LOGGER.info("Creating MLRun project.")
        mlrun_project = self._get_mlrun_project(project)
        mlrun_function = self._get_mlrun_function(
            mlrun_project, dhcore_function.name, function_source, function_specs, parameters
        )

        # Execute function
        LOGGER.info("Executing function.")
        if action == "mlrun":
            execution_results = self._run_job(mlrun_function)
        else:
            msg = f"Task {action} not allowed for MLRun runtime"
            LOGGER.error(msg)
            raise EntityError(msg)

        # Parse execution results
        LOGGER.info("Parsing execution results.")
        return self._parse_execution_results(execution_results)

    ####################
    # Dhcore function helpers
    ####################

    def _get_dhcore_function(self, project: str, spec: dict) -> Function:
        """
        Get DHCore function.

        Parameters
        ----------
        project : str
            Name of the project.
        spec : dict
            Run specs.

        Returns
        -------
        Function
            DHCore function.
        """
        function_name = spec.get("task").split(":")[0].split("+")[0]
        return get_function(project, function_name)

    def _save_function_source(self, function: Function) -> str:
        """
        Save function source.

        Parameters
        ----------
        function : Function
            DHCore function.

        Returns
        -------
        path
            Path to the function source.
        """
        path = self.root / function.spec.build.get("origin_filename")
        path.write_text(decode_string(function.spec.build.get("functionSourceCode")))
        return str(path)

    def _parse_function_specs(self, function: Function) -> dict:
        """
        Parse function specs.

        Parameters
        ----------
        function : Function
            DHCore function.

        Returns
        -------
        dict
            Function specs.
        """
        return {
            "image": function.spec.image,
            "tag": function.spec.tag,
            "handler": function.spec.handler,
            "command": function.spec.command,
            "requirements": function.spec.requirements,
        }

    ####################
    # MLRun helpers
    ####################

    @staticmethod
    def _get_mlrun_project(project_name: str) -> MlrunProject:
        """
        Get MLRun project.

        Parameters
        ----------
        project_name : str
            Name of the project.

        Returns
        -------
        MlrunProject
            MLRun project.
        """
        return mlrun.get_or_create_project(project_name, "./", user_project=True)

    @staticmethod
    def _get_mlrun_function(
        project: MlrunProject,
        function_name: str,
        function_source: str,
        function_specs: dict,
        parameters: dict,
    ) -> BaseRuntime:
        """
        Get MLRun function.

        Parameters
        ----------
        project : MlrunProject
            MLRun project.
        function_name : str
            Name of the function.
        function_source : str
            Path to the function source.
        function_specs : dict
            Function specs.
        parameters : dict
            Function parameters.

        Returns
        -------
        BaseRuntime
            MLRun function.
        """
        kwargs = {
            **parameters,
            **function_specs,
        }
        project.set_function(
            function_source,
            name=function_name,
            **kwargs,
        )
        project.save()
        return project.get_function(function_name)

    ####################
    # Execution helpers
    ####################

    @staticmethod
    def _run_job(function: BaseRuntime) -> BaseRuntime:
        """
        Run MLRun job.

        Parameters
        ----------
        function : BaseRuntime
            MLRun function.

        Returns
        -------
        dict
            Execution results.
        """
        return function.run(local=True)

    ####################
    # Results helpers
    ####################

    @staticmethod
    def _parse_execution_results(execution_results: BaseRuntime) -> dict:
        """
        Parse execution results.

        Parameters
        ----------
        execution_results : BaseRuntime
            Execution results.

        Returns
        -------
        dict
            Parsed execution results.
        """
        return {
            "status": execution_results.status,
            "result": execution_results.to_dict(),
        }
