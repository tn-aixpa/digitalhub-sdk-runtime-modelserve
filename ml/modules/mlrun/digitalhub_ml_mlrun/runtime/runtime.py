"""
Runtime class for running MLRun functions.
"""
from __future__ import annotations

import typing
from pathlib import Path

import mlrun
from digitalhub_core.entities._base.status import State
from digitalhub_core.entities.artifacts.crud import new_artifact
from digitalhub_core.entities.artifacts.utils import get_artifact_info
from digitalhub_core.entities.dataitems.crud import create_dataitem
from digitalhub_core.entities.dataitems.utils import get_dataitem_info
from digitalhub_core.entities.functions.crud import get_function
from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import decode_string
from digitalhub_core.utils.logger import LOGGER

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_core.entities.dataitems.entity import Dataitem
    from digitalhub_core.entities.functions.entity import Function
    from mlrun.projects import MlrunProject
    from mlrun.runtimes import BaseRuntime
    from mlrun.runtimes.base import RunObject


class RuntimeMLRun(Runtime):
    """
    Runtime MLRun class.
    """

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
        function_args = spec.get("parameters", {})

        # Create MLRun project
        LOGGER.info("Creating MLRun project.")
        mlrun_project = self._get_mlrun_project(project)
        mlrun_function = self._get_mlrun_function(
            mlrun_project,
            dhcore_function.name,
            function_source,
            function_specs,
        )

        # Execute function
        LOGGER.info("Executing function.")
        if action == "mlrun":
            execution_results = self._run_job(mlrun_function, function_args)
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
        func = spec.get("function").split("://")[1].split("/")[1]
        function_name, function_version = func.split(":")
        LOGGER.info(f"Getting function {function_name}:{function_version}.")
        return get_function(project, function_name, function_version)

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
        self.root_path.mkdir(parents=True, exist_ok=True)
        path = self.root_path / function.spec.build.get("origin_filename")
        path.write_text(decode_string(function.spec.build.get("function_source_code")))
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
        return mlrun.get_or_create_project(project_name, "./")

    @staticmethod
    def _get_mlrun_function(
        project: MlrunProject,
        function_name: str,
        function_source: str,
        function_specs: dict,
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

        Returns
        -------
        BaseRuntime
            MLRun function.
        """
        project.set_function(
            function_source,
            name=function_name,
            **function_specs,
        )
        project.save()
        return project.get_function(function_name)

    ####################
    # Execution helpers
    ####################

    @staticmethod
    def _run_job(function: BaseRuntime, function_args: dict) -> RunObject:
        """
        Run MLRun job.

        Parameters
        ----------
        function : BaseRuntime
            MLRun function.
        function_args : dict
            Function arguments.

        Returns
        -------
        dict
            Execution results.
        """
        function_args["local"] = True
        return mlrun.run_function(function, **function_args)

    ####################
    # Results helpers
    ####################

    def _parse_execution_results(self, execution_results: RunObject) -> dict:
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
        try:
            results = {}

            # Check execution state
            results["state"] = self._map_state(execution_results.status.state)

            # Get artifacts
            artifacts = self._parse_artifacts(execution_results.status.artifacts)
            if artifacts:
                results["artifacts"] = [get_artifact_info(i) for i in artifacts]

            # Get dataitems
            dataitems = self._parse_dataitems(execution_results.status.artifacts)
            if dataitems:
                results["dataitems"] = [get_dataitem_info(i) for i in dataitems]

            # Get timings
            results["timings"] = {
                "start": execution_results.status.start_time,
                "updated": execution_results.status.last_update,
            }

            # Embed execution results
            results["mlrun_results"] = execution_results.to_dict()

            # Return results
            return results
        except Exception:
            msg = "Something got wrong during execution results parsing."
            LOGGER.exception(msg)
            raise RuntimeError(msg)

    @staticmethod
    def _map_state(state: str) -> str:
        """
        Map MLRun state to digitalhub state.

        Parameters
        ----------
        state : str
            MLRun state.

        Returns
        -------
        str
            Mapped digitalhub state.
        """
        _map_state = {
            "completed": State.COMPLETED.value,
            "error": State.ERROR.value,
            "running": State.RUNNING.value,
            "created": State.CREATED.value,
            "pending": State.PENDING.value,
            "unknown": State.ERROR.value,
            "aborted": State.STOP.value,
            "aborting": State.STOP.value,
        }
        return _map_state.get(state, State.ERROR.value)

    ####################
    # Artifacts helpers
    ####################

    def _parse_artifacts(self, mlrun_outputs: list[dict]) -> list[Artifact]:
        """
        Filter out models and datasets from MLRun outputs and create DHCore artifacts.

        Parameters
        ----------
        mlrun_outputs : list[dict]
            MLRun outputs.

        Returns
        -------
        list[Artifact]
            DHCore artifacts list.
        """
        outputs = [i for i in mlrun_outputs if i.get("kind") not in ["model", "dataset"]]
        return [self._create_artifact(j) for j in outputs]

    @staticmethod
    def _create_artifact(mlrun_artifact: dict) -> Artifact:
        """
        New artifact.

        Parameters
        ----------
        mlrun_arti : dict
            Mlrun artifact.

        Returns
        -------
        dict
            Artifact info.
        """
        try:
            kwargs = {}
            kwargs["project"] = mlrun_artifact.get("metadata", {}).get("project")
            kwargs["name"] = mlrun_artifact.get("metadata", {}).get("key")
            kwargs["kind"] = "artifact"
            kwargs["target_path"] = mlrun_artifact.get("spec", {}).get("target_path")
            kwargs["size"] = mlrun_artifact.get("spec", {}).get("size")
            kwargs["hash"] = mlrun_artifact.get("spec", {}).get("hash")
            return new_artifact(**kwargs)
        except Exception:
            msg = "Something got wrong during artifact creation."
            LOGGER.exception(msg)
            raise RuntimeError(msg)

    ####################
    # Dataitems helpers
    ####################

    def _parse_dataitems(self, mlrun_outputs: list[dict]) -> list[Dataitem]:
        """
        Filter out datasets from MLRun outputs and create DHCore dataitems.

        Parameters
        ----------
        mlrun_outputs : list[dict]
            MLRun outputs.

        Returns
        -------
        list[Dataitem]
            DHCore dataitems list.
        """
        outputs = [i for i in mlrun_outputs if i.get("kind") == "dataset"]
        return [self._create_artifact(j) for j in outputs]

    def _create_dataitem(self, mlrun_output: dict) -> Dataitem:
        """
        New dataitem.

        Parameters
        ----------
        mlrun_output : dict
            Mlrun output.

        Returns
        -------
        dict
            Dataitem info.
        """
        try:
            # Create dataitem
            kwargs = {}
            kwargs["project"] = mlrun_output.get("metadata", {}).get("project")
            kwargs["name"] = mlrun_output.get("metadata", {}).get("key")
            kwargs["kind"] = "dataitem"
            kwargs["path"] = mlrun_output.get("spec", {}).get("target_path")
            kwargs["schema"] = mlrun_output.get("spec", {}).get("schema", {}).get("fields")
            dataitem = create_dataitem(**kwargs)

            # Add sample preview
            header = mlrun_output.get("spec", {}).get("header", [])
            sample_data = mlrun_output.get("status", {}).get("preview", [[]])
            dataitem.status.preview = self._pivot_preview(header, sample_data)

            # Save dataitem in core and return it
            dataitem.save()
            return dataitem
        except Exception:
            msg = "Something got wrong during dataitem creation."
            LOGGER.exception(msg)
            raise RuntimeError(msg)

    @staticmethod
    def _pivot_preview(columns: list, data: list[list]) -> list[list]:
        """
        Pivot preview from MLRun.

        Parameters
        ----------
        columns : list
            Columns.
        data : list[list]
            Data preview.

        Returns
        -------
        list[list]
            Pivoted preview.
        """
        ordered_data = [[j[idx] for j in data] for idx, _ in enumerate(columns)]
        return [{"name": c, "value": d} for c, d in zip(columns, ordered_data)]
