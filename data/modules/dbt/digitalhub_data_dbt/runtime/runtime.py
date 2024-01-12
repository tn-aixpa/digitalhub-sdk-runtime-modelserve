"""
Runtime DBT module.
"""
from __future__ import annotations

import os
import typing
from pathlib import Path

import psycopg2
from dbt.cli.main import dbtRunner, dbtRunnerResult
from digitalhub_core.entities._base.status import State
from digitalhub_core.entities.dataitems.crud import create_dataitem, get_dataitem
from digitalhub_core.entities.dataitems.utils import get_dataitem_info
from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.exceptions import BackendError, EntityError
from digitalhub_core.utils.generic_utils import build_uuid, decode_string
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data_dbt.runtime.dbt_utils import (
    generate_dbt_profile_yml,
    generate_dbt_project_yml,
    generate_inputs_conf,
    generate_outputs_conf,
)
from digitalhub_data_dbt.runtime.parse_utils import ParsedResults, get_schema, parse_results, pivot_data
from psycopg2 import sql

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.dataitems.entity import Dataitem


HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE = os.getenv("POSTGRES_DATABASE")
SCHEMA = os.getenv("POSTGRES_SCHEMA", "public")


class RuntimeDBT(Runtime):
    """
    Runtime DBT class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.root_dir = Path("/tmp/dbt_run")
        self.model_dir = self.root_dir / "models"
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

        Returns
        -------
        dict
            Status of the executed run.
        """

        # Get action
        action = self._get_action(run)

        # Handle unknown task kind
        if action not in ["transform"]:
            msg = f"Task {action} not allowed for DBT runtime"
            LOGGER.error(msg)
            raise EntityError(msg)

        # Execute action
        return self.execute(run)

    ####################
    # TRANSFORM TASK
    ####################

    def execute(self, run: dict) -> dict:
        """
        Execute task.

        Returns
        -------
        dict
            Status of the executed run.
        """

        # Get run specs
        LOGGER.info("Starting task.")
        spec = run.get("spec")
        project = run.get("project")

        # Parse inputs/outputs and decode sql code
        LOGGER.info("Parsing inputs and output.")
        self._get_inputs(spec.get("inputs", {}).get("dataitems", []), project)
        output = self._get_output_table_name(spec.get("outputs", {}).get("dataitems", []))
        query = self._get_sql(spec)

        # Setup environment
        LOGGER.info("Setting up environment for dbt execution.")
        uuid = build_uuid()
        self.setup(output, uuid, project, query)

        # Execute function
        LOGGER.info("Executing dbt project.")
        execution_results = self.transform(output)

        # Parse results
        LOGGER.info("Parsing results.")
        parsed_result = parse_results(execution_results, output, project)

        # Create dataitem
        LOGGER.info("Creating output dataitem.")
        dataitem = self._create_dataitem(parsed_result, project, uuid)

        # Clean environment
        self.cleanup()

        # Return run status
        LOGGER.info("Task completed, returning run status.")
        return {
            "dataitems": [get_dataitem_info(dataitem)],
            "timings": parsed_result.timings,
            "state": State.COMPLETED.value,
        }

    ####################
    # Parse inputs/outputs
    ####################

    def _get_inputs(self, inputs: list, project: str) -> None:
        """
        Parse inputs from run spec and materialize dataitems in postgres.

        Parameters
        ----------
        inputs : list
            The list of inputs.
        project : str
            The project name.

        Returns
        -------
        None
        """
        for name in inputs:
            # Get dataitem objects from core
            di = self._get_dataitem(name, project)

            # Register dataitem in a dict to be used for inputs confs generation
            self._input_dataitems.append({"name": di.name, "id": di.id})

            # Materialize dataitem in postgres
            table = self._materialize_dataitem(di, name)

            # Save versioned table name to be used for cleanup
            self._versioned_tables.append(table)

    @staticmethod
    def _get_dataitem(name: str, project: str) -> Dataitem:
        """
        Get dataitem from core.

        Parameters
        ----------
        name : str
            The dataitem name.
        project : str
            The project name.

        Returns
        -------
        Dataitem
            The dataitem.

        Raises
        ------
        BackendError
            If dataitem is not found.
        """
        try:
            LOGGER.info(f"Getting dataitem '{name}'")
            return get_dataitem(project, name)
        except BackendError:
            msg = f"Dataitem {name} not found."
            LOGGER.exception(msg)
            raise BackendError(msg)

    @staticmethod
    def _materialize_dataitem(dataitem: Dataitem, name: str) -> str:
        """
        Materialize dataitem in postgres.

        Parameters
        ----------
        dataitem : Dataitem
            The dataitem.
        name : str
            The dataitem name.

        Returns
        -------
        str
            The materialized table name.

        Raises
        ------
        EntityError
            If something got wrong during dataitem materialization.
        """
        try:
            table_name = f"{name}_v{dataitem.id}"
            LOGGER.info(f"Materializing dataitem '{name}' as '{table_name}'.")
            target_path = f"sql://{DATABASE}/{SCHEMA}/{table_name}"
            dataitem.write_df(target_path, if_exists="replace")
            return table_name
        except Exception:
            msg = f"Something got wrong during dataitem {name} materialization."
            LOGGER.exception(msg)
            raise EntityError(msg)

    @staticmethod
    def _get_output_table_name(outputs: list) -> str:
        """
        Get output table name from run spec.

        Parameters
        ----------
        outputs : list
            The list of outputs.

        Returns
        -------
        str
            The output dataitem/table name.

        Raises
        ------
        RuntimeError
            If outputs are not a list of one dataitem.
        """
        if not isinstance(outputs, list) or len(outputs) > 1:
            msg = "Outputs must be a list of exactly one dataitem."
            LOGGER.error(msg)
            raise RuntimeError(msg)
        return str(outputs[0])

    def _get_sql(self, spec: dict) -> str:
        """
        Get sql code from run spec.

        Parameters
        ----------
        spec : dict
            The run spec.

        Returns
        -------
        str
            The sql code.

        Raises
        ------
        RuntimeError
            If sql code is not a valid string.
        """
        try:
            return decode_string(spec.get("sql"))
        except Exception:
            msg = "Sql code must be a valid string."
            LOGGER.exception(msg)
            raise RuntimeError(msg)

    ####################
    # Setup environment
    ####################

    def setup(self, output: str, uuid: str, project: str, query: str) -> None:
        """
        Initialize a dbt project with a model and a schema definition.

        Parameters
        ----------
        output : str
            The output table name.
        uuid : str
            The uuid of the model for outputs versioning.
        project : str
            The project name.
        sql : str
            The sql code.

        Returns
        -------
        None
        """
        # Create directories
        self.model_dir.mkdir(exist_ok=True, parents=True)

        # Generate profile yaml file
        generate_dbt_profile_yml(self.root_dir)

        # Generate project yaml file
        generate_dbt_project_yml(self.root_dir, self.model_dir, project.replace("-", "_"))

        # Generate outputs confs
        generate_outputs_conf(self.model_dir, query, output, uuid)

        # Generate inputs confs for every dataitem
        for di in self._input_dataitems:
            generate_inputs_conf(self.model_dir, di["name"], di["id"])

    ####################
    # Execute function
    ####################

    def transform(self, output: str) -> dbtRunnerResult:
        """
        Execute a dbt project with the specified outputs.
        It initializes a dbt runner, cleans the project and runs it.

        Parameters
        ----------
        output : str
            The output table name.

        Returns
        -------
        dbtRunnerResult
            An object representing the result of the dbt execution.
        """
        current_dir = os.getcwd()
        os.chdir(self.root_dir)
        dbt = dbtRunner()
        dbt.invoke("clean")
        cli_args = ["run", "--select", f"{output}"]
        res = dbt.invoke(cli_args)
        os.chdir(current_dir)
        return res

    ####################
    # Produce outputs
    ####################

    def _create_dataitem(self, result: ParsedResults, project: str, uuid: str) -> Dataitem:
        """
        Create new dataitem.

        Parameters
        ----------
        result : ParsedResults
            The parsed results.
        project : str
            The project name.
        uuid : str
            The uuid of the model for outputs versioning.

        Returns
        -------
        list[dict]
            The output dataitem infos.

        Raises
        ------
        RuntimeError
            If something got wrong during dataitem creation.
        """
        try:
            # Get columns and data sample from dbt results
            columns, data = self._get_data_sample(result.name, uuid)

            # Prepare dataitem kwargs
            kwargs = {}
            kwargs["project"] = project
            kwargs["name"] = result.name
            kwargs["kind"] = "dataitem"
            kwargs["path"] = result.path
            kwargs["uuid"] = uuid
            kwargs["schema"] = get_schema(columns)
            kwargs["raw_code"] = result.raw_code
            kwargs["compiled_code"] = result.compiled_code

            # Create dataitem
            dataitem = create_dataitem(**kwargs)

            # Update dataitem status with preview
            dataitem.status.preview = pivot_data(columns, data)

            # Save dataitem in core and return it
            dataitem.save()
            return dataitem

        except Exception:
            msg = "Something got wrong during dataitem creation."
            LOGGER.exception(msg)
            raise RuntimeError(msg)

    def _get_data_sample(self, table_name: str, uuid: str) -> None:
        """
        Get columns and data sample from dbt results.

        Parameters
        ----------
        table_name : str
            The output table name.
        uuid : str
            The uuid of the model for outputs versioning.

        Returns
        -------
        None
        """
        LOGGER.info("Getting columns and data sample from dbt results.")
        try:
            connection = self._get_connection()
            query = sql.SQL("SELECT * FROM {table} LIMIT 5;").format(table=sql.Identifier(f"{table_name}_v{uuid}"))
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    columns = cursor.description
                    data = cursor.fetchall()
            return columns, data
        except Exception:
            msg = "Something got wrong during data fetching."
            LOGGER.exception(msg)
            raise RuntimeError(msg)
        finally:
            LOGGER.info("Closing connection to postgres.")
            connection.close()

    ####################
    # Cleanup
    ####################

    def cleanup(self) -> None:
        """
        Cleanup environment.

        Returns
        -------
        None
        """
        LOGGER.info("Cleaning up environment.")
        try:
            connection = self._get_connection()
            with connection:
                with connection.cursor() as cursor:
                    for table in self._versioned_tables:
                        LOGGER.info(f"Dropping table '{table}'.")
                        query = sql.SQL("DROP TABLE {table}").format(table=sql.Identifier(table))
                        cursor.execute(query)
        except Exception:
            msg = "Something got wrong during environment cleanup."
            LOGGER.exception(msg)
            raise RuntimeError(msg)
        finally:
            LOGGER.info("Closing connection to postgres.")
            connection.close()

    @staticmethod
    def _get_connection() -> psycopg2.extensions.connection:
        """
        Create a connection to postgres and return a session with autocommit enabled.

        Returns
        -------
        psycopg2.extensions.connection
            The connection to postgres.

        Raises
        ------
        RuntimeError
            If something got wrong during connection to postgres.
        """
        try:
            LOGGER.info("Connecting to postgres.")
            return psycopg2.connect(
                host=HOST,
                port=PORT,
                database=DATABASE,
                user=USER,
                password=PASSWORD,
            )
        except Exception:
            msg = "Something got wrong during connection to postgres."
            LOGGER.exception(msg)
            raise RuntimeError(msg)
