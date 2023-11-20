"""
Runtime DBT module.
"""
from __future__ import annotations

import os
import typing
from dataclasses import dataclass
from pathlib import Path

import psycopg2
from dbt.cli.main import dbtRunner, dbtRunnerResult
from digitalhub_core.entities._base.status import State
from digitalhub_core.entities.dataitems.crud import get_dataitem, new_dataitem
from digitalhub_core.runtimes.base import Runtime
from digitalhub_core.utils.exceptions import BackendError, EntityError
from digitalhub_core.utils.generic_utils import build_uuid, decode_string, encode_string
from digitalhub_core.utils.logger import LOGGER
from psycopg2 import sql as psql

if typing.TYPE_CHECKING:
    from dbt.contracts.results import RunResult
    from digitalhub_core.entities.dataitems.entity import Dataitem

####################
# ENV
####################
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA", "public")

####################
# Templates
####################

PROJECT_TEMPLATE = """
name: "{}"
version: "1.0.0"
config-version: 2
profile: "postgres"
model-paths: ["{}"]
models:
"""

MODEL_TEMPLATE_UUID = """
models:
  - name: {}
    latest_uuid: {}
    uuids:
        - v: {}
          config:
            materialized: table
"""

MODEL_TEMPLATE_VERSION = """
models:
  - name: {}
    latest_version: {}
    versions:
        - v: {}
          config:
            materialized: table
"""

PROFILE_TEMPLATE = f"""
postgres:
    outputs:
        dev:
            type: postgres
            host: {POSTGRES_HOST}
            user: {POSTGRES_USER}
            pass: {POSTGRES_PASSWORD}
            port: {POSTGRES_PORT}
            dbname: {POSTGRES_DATABASE}
            schema: {POSTGRES_SCHEMA}
    target: dev
"""

####################
# Results parsing
####################


@dataclass
class ParsedResults:
    """
    Parsed results class.
    """

    name: str
    path: str
    raw_code: str
    compiled_code: str
    timings: dict


####################
# Runtime
####################


class RuntimeDBT(Runtime):
    """
    Runtime DBT class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.root_dir = Path("dbt_run")
        self.model_dir = self.root_dir / "models"
        self._table_to_drop = []

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
        project = run.get("metadata").get("project")

        # Parse inputs/outputs
        LOGGER.info("Parsing inputs and output.")
        inputs = self.parse_inputs(spec.get("inputs", {}).get("dataitems", []), project)
        output = self.parse_outputs(spec.get("outputs", {}).get("dataitems", []))

        # Setup environment
        LOGGER.info("Setting up environment for dbt execution.")
        uuid = build_uuid()
        self.setup(inputs, output, uuid, project, spec.get("sql"))

        # Execute function
        LOGGER.info("Executing dbt project.")
        execution_results = self.transform(output)

        # Parse results
        LOGGER.info("Parsing results.")
        parsed_result = self.parse_results(execution_results, output, project)

        # Create dataitem
        LOGGER.info("Creating output dataitem.")
        dataitem = self.create_dataitem(parsed_result, project, uuid)

        # Clean environment
        self.cleanup()

        # Return run status
        LOGGER.info("Task completed, returning run status.")
        return {
            **self._get_dataitem_info(output, dataitem),
            **parsed_result.timings,
            "state": State.COMPLETED.value,
        }

    ####################
    # Parse inputs/outputs
    ####################

    def parse_inputs(self, inputs: list, project: str) -> list:
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
        list
            The list of inputs dataitems names.
        """
        for name in inputs:
            dataitem = self._get_dataitem(name, project)
            table = self._materialize_dataitem(dataitem, name)
            self._table_to_drop.append(table)
        return inputs

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
            return get_dataitem(project, name)
        except BackendError as err:
            msg = f"Dataitem {name} not found. Error: {err.args[0]}."
            LOGGER.error(msg)
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
            target_path = f"sql://{POSTGRES_DATABASE}/{POSTGRES_SCHEMA}/{table_name}"
            LOGGER.info(f"Materializing dataitem {name} in postgres as {target_path}.")
            dataitem.write_df(target_path, if_exists="replace")
            return table_name
        except Exception as err:
            msg = f"Something got wrong during dataitem {name} materialization. Error: {err.args[0]}."
            LOGGER.error(msg)
            raise EntityError(msg)

    def parse_outputs(self, outputs: list) -> str:
        """
        Parse outputs from run spec.

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
            msg = "Outputs must be a list of one dataitem."
            LOGGER.error(msg)
            raise RuntimeError(msg)
        return str(outputs[0])

    ####################
    # Setup environment
    ####################

    def setup(self, inputs: list, output: str, uuid: str, project: str, sql: str) -> None:
        """
        Initialize a dbt project with a model and a schema definition.

        Parameters
        ----------
        inputs : list
            The list of inputs.
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
        self.generate_dbt_profile_yml()

        # Generate project yaml file
        self.generate_dbt_project_yml(project)

        # Generate outputs confs
        self.generate_outputs_conf(sql, output, uuid)

        # Generate inputs confs
        self.generate_inputs_conf(inputs, project)

    def generate_dbt_profile_yml(self) -> None:
        """
        Create dbt profiles.yml

        Returns
        -------
        None
        """
        profiles_path = self.root_dir / "profiles.yml"
        profiles_path.write_text(PROFILE_TEMPLATE)

    def generate_dbt_project_yml(self, project: str) -> None:
        """
        Create dbt_project.yml from 'dbt'

        Parameters
        ----------
        project : str
            The project name.

        Returns
        -------
        None
        """
        project_path = self.root_dir / "dbt_project.yml"
        project_path.write_text(PROJECT_TEMPLATE.format(project.replace("-", "_"), self.model_dir.name))

    def generate_outputs_conf(self, sql: str, output: str, uuid: str) -> None:
        """
        Write sql code for the model and write schema
        and version detail for outputs versioning

        Parameters
        ----------
        sql : str
            The sql code.
        output : str
            The output table name.
        uuid : str
            The uuid of the model for outputs versioning.

        Returns
        -------
        None
        """
        sql = decode_string(sql)

        sql_path = self.model_dir / f"{output}.sql"
        sql_path.write_text(sql)

        output_path = self.model_dir / f"{output}.yml"
        output_path.write_text(MODEL_TEMPLATE_VERSION.format(output, uuid, uuid))

    def generate_inputs_conf(self, inputs: list, project: str) -> None:
        """
        Generate inputs confs dependencies for dbt project.

        Parameters
        ----------
        project : str
            The project name.
        inputs : list
            The list of inputs dataitems names.

        Returns
        -------
        None
        """
        for name in inputs:
            # Get dataitem from core
            response = get_dataitem(project, name)
            uuid = response.id

            # write schema and version detail for inputs versioning
            input_path = self.model_dir / f"{name}.sql"
            input_path.write_text(MODEL_TEMPLATE_UUID.format(name, uuid, uuid))

            # write also sql select for the schema
            sql_path = self.model_dir / f"{name}_v{uuid}.sql"
            sql_path.write_text(f'SELECT * FROM "{name}_v{uuid}"')

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
        os.chdir(self.root_dir)
        dbt = dbtRunner()
        dbt.invoke("clean")
        cli_args = ["run", "--select", f"{output}"]
        res = dbt.invoke(cli_args)
        os.chdir("..")
        return res

    ####################
    # Results parsing
    ####################

    def parse_results(self, run_result: dbtRunnerResult, output: str, project: str) -> ParsedResults:
        """
        Parse dbt results.

        Parameters
        ----------
        run_result : dbtRunnerResult
            The dbt result.
        output : str
            The output table name.
        project : str
            The project name.

        Returns
        -------
        ParsedResults
            Parsed results.
        """
        result: RunResult = self.validate_results(run_result, output, project)
        try:
            path = self.get_path(result)
            raw_code = self.get_raw_code(result)
            compiled_code = self.get_compiled_code(result)
            timings = self.get_timings(result)
            name = result.node.name
        except Exception as err:
            msg = f"Something got wrong during results parsing. Error: {err.args[0]}."
            LOGGER.error(msg)
            raise RuntimeError(msg)
        return ParsedResults(name, path, raw_code, compiled_code, timings)

    def validate_results(self, run_result: dbtRunnerResult, output: str, project: str) -> RunResult:
        """
        Parse dbt results.

        Parameters
        ----------
        run_result : dbtRunnerResult
            The dbt result.
        output : str
            The output table name.
        project : str
            The project name.

        Returns
        -------
        RunResult
            Run result.

        Raises
        ------
        RuntimeError
            If something got wrong during function execution.
        """
        try:
            # Take last result, final result of the query
            result: RunResult = run_result.result[-1]
        except IndexError:
            msg = "No results found."
            LOGGER.error(msg)
            raise RuntimeError(msg)

        if not result.status.value == "success":
            msg = f"Function execution failed: {result.status.value}."
            LOGGER.error(msg)
            raise RuntimeError(msg)

        if not result.node.package_name == project.replace("-", "_"):
            msg = f"Wrong project name. Got {result.node.package_name}, expected {project.replace('-', '_')}."
            LOGGER.error(msg)
            raise RuntimeError(msg)

        if not result.node.name == output:
            msg = f"Wrong output name. Got {result.node.name}, expected {output}."
            LOGGER.error(msg)
            raise RuntimeError(msg)

        return result

    def get_path(self, result: RunResult) -> str:
        """
        Get path from dbt result (sql://database/schema/table).

        Parameters
        ----------
        result : RunResult
            The dbt result.

        Returns
        -------
        str
            SQL path.
        """
        components = result.node.relation_name.replace('"', "")
        components = "/".join(components.split("."))
        return f"sql://{components}"

    def get_raw_code(self, result: RunResult) -> str:
        """
        Get raw code from dbt result.

        Parameters
        ----------
        result : RunResult
            The dbt result.

        Returns
        -------
        str
            The raw code.
        """
        return encode_string(str(result.node.raw_code))

    def get_compiled_code(self, result: RunResult) -> str:
        """
        Get compiled code from dbt result.

        Parameters
        ----------
        result : RunResult
            The dbt result.

        Returns
        -------
        str
            The compiled code.
        """
        return encode_string(str(result.node.compiled_code))

    def get_timings(self, result: RunResult) -> dict:
        """
        Get timings from dbt result.

        Parameters
        ----------
        result : RunResult
            The dbt result.

        Returns
        -------
        dict
            A dictionary containing timings.
        """
        compile_timing = None
        execute_timing = None
        for entry in result.timing:
            if entry.name == "compile":
                compile_timing = entry
            elif entry.name == "execute":
                execute_timing = entry
        if (
            (compile_timing is None or execute_timing is None)
            or (execute_timing.started_at is None or execute_timing.completed_at is None)
            or (compile_timing.started_at is None or compile_timing.completed_at is None)
        ):
            msg = "Something got wrong during timings parsing."
            LOGGER.error(msg)
            raise RuntimeError(msg)
        return {
            "timing": {
                "compile": {
                    "started_at": compile_timing.started_at.isoformat(),
                    "completed_at": compile_timing.completed_at.isoformat(),
                },
                "execute": {
                    "started_at": execute_timing.started_at.isoformat(),
                    "completed_at": execute_timing.completed_at.isoformat(),
                },
            }
        }

    ####################
    # CRUD
    ####################

    def create_dataitem(self, result: ParsedResults, project: str, uuid: str) -> Dataitem | None:
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
        Dataitem
            The dataitem.

        Raises
        ------
        RuntimeError
            If something got wrong during dataitem creation.
        """
        try:
            return new_dataitem(
                project=project,
                name=result.name,
                kind="dataitem",
                path=result.path,
                uuid=uuid,
                raw_code=result.raw_code,
                compiled_code=result.compiled_code,
            )
        except Exception as err:
            msg = f"Something got wrong during dataitem creation. Error: {err.args[0]}."
            LOGGER.error(msg)
            raise RuntimeError(msg)

    @staticmethod
    def _get_dataitem_info(output: str, dataitem: Dataitem) -> dict:
        """
        Create dataitem info.

        Parameters
        ----------
        output : str
            The output table name.
        dataitem : Dataitem
            The dataitem.
        """
        kind = dataitem.kind
        project = dataitem.metadata.project
        name = dataitem.metadata.name
        version = dataitem.id
        return {
            "dataitems": [
                {
                    "key": output,
                    "kind": kind,
                    "id": f"store://{project}/dataitems/{kind}/{name}:{version}",
                }
            ]
        }

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
        connection = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DATABASE,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
        connection.set_session(autocommit=True)
        for table in self._table_to_drop:
            with connection.cursor() as cursor:
                query = psql.SQL("DROP TABLE {table}").format(table=psql.Identifier(table))
                cursor.execute(query)
        connection.close()
