"""
Runtime DBT module.
"""
from __future__ import annotations

import typing
from pathlib import Path
from typing import Callable

from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.generic_utils import build_uuid
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data.entities.dataitems.crud import get_dataitem_from_key
from digitalhub_data.runtimes.results import RunResultsData
from digitalhub_data_dbt.utils.cleanup import cleanup
from digitalhub_data_dbt.utils.configuration import (
    generate_dbt_profile_yml,
    generate_dbt_project_yml,
    generate_inputs_conf,
    generate_outputs_conf,
)
from digitalhub_data_dbt.utils.functions import transform
from digitalhub_data_dbt.utils.inputs import get_dataitem_, get_output_table_name, get_sql, materialize_dataitem
from digitalhub_data_dbt.utils.outputs import build_status, create_dataitem_, parse_results

if typing.TYPE_CHECKING:
    from dbt.contracts.results import RunResult
    from digitalhub_data.entities.dataitems.entity import Dataitem
    from digitalhub_data_dbt.utils.outputs import ParsedResults


class RuntimeDBT(Runtime):
    """
    Runtime DBT class.
    """

    allowed_actions = ["transform"]

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()

        # Paths
        self.root_dir = Path("/tmp/dbt_run")
        self.model_dir = self.root_dir / "models"

        # UUID for output dataitem and dbt execution
        self.uuid = build_uuid()

        # Registries
        self._input_dataitems: list[dict[str, str]] = []
        self._versioned_tables: list[str] = []

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
        func = self._get_function(action)

        LOGGER.info("Starting task.")
        spec = run.get("spec")
        project = run.get("project")

        LOGGER.info("Collecting inputs.")
        self._collect_inputs(spec, project)

        LOGGER.info("Configure execution.")
        output_table = self._configure_execution(spec, project)

        LOGGER.info("Executing run.")
        results = self._execute(func, output_table, self.root_dir)

        LOGGER.info("Collecting outputs.")
        outputs = self._collect_outputs(results, output_table, project)
        status = build_status(outputs, results)

        LOGGER.info("Clean up environment.")
        self._cleanup()

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
        if action == "transform":
            return transform
        raise NotImplementedError

    @staticmethod
    def results(run_status: dict) -> RunResultsData:
        """
        Get run results.

        Returns
        -------
        RunResultsData
            Run results.
        """
        dataitems = run_status.get("dataitems", [])
        dataitem_objs = [get_dataitem_from_key(dti.get("id")) for dti in dataitems]
        return RunResultsData(dataitems=dataitem_objs)

    ####################
    # Inputs
    ####################

    def _collect_inputs(self, spec: dict, project: str) -> None:
        """
        Parse inputs from run spec and materialize dataitems in postgres.

        Parameters
        ----------
        spec : dict
            Run spec dict.
        project : str
            The project name.

        Returns
        -------
        None
        """
        # Collect input dataitems
        inputs = spec.get("inputs", {}).get("dataitems", [])
        for name in inputs:
            # Get dataitem objects from core
            di = get_dataitem_(name, project)

            # Register dataitem in a dict to be used for inputs confs generation
            self._input_dataitems.append({"name": di.name, "id": di.id})

            # Materialize dataitem in postgres
            table = materialize_dataitem(di, name)

            # Save versioned table name to be used for cleanup
            self._versioned_tables.append(table)

    ####################
    # Configuration
    ####################

    def _configure_execution(self, spec: dict, project: str) -> str:
        """
        Initialize a dbt project with a model and a schema definition.

        Parameters
        ----------
        spec : str
            Run spec dict.
        project : str
            The project name.

        Returns
        -------
        str
            Output table name.
        """

        output_table = get_output_table_name(spec)
        query = get_sql(spec)

        # Create directories
        self.model_dir.mkdir(exist_ok=True, parents=True)

        # Generate profile yaml file
        generate_dbt_profile_yml(self.root_dir)

        # Generate project yaml file
        generate_dbt_project_yml(self.root_dir, self.model_dir, project.replace("-", "_"))

        # Generate outputs confs
        generate_outputs_conf(self.model_dir, query, output_table, self.uuid)

        # Generate inputs confs for every dataitem
        for di in self._input_dataitems:
            generate_inputs_conf(self.model_dir, di["name"], di["id"])

        return output_table

    ####################
    # Outputs
    ####################

    def _collect_outputs(self, results: RunResult, output_table: str, project: str) -> tuple[ParsedResults, Dataitem]:
        """
        Collect outputs.

        Parameters
        ----------
        results : dict
            The dbt run results.
        output_table : str
            Output table name.
        project : str
            The project name.

        Returns
        -------
        list
            List of artifacts paths.
        """
        parsed_result = parse_results(results, output_table, project)
        dataitem = create_dataitem_(parsed_result, project, self.uuid)
        return parsed_result, dataitem

    ####################
    # Cleanup
    ####################

    def _cleanup(self) -> None:
        """
        Cleanup environment.

        Returns
        -------
        None
        """
        cleanup(self._versioned_tables)
