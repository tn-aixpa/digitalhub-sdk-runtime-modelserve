"""
Runtime job DBT module.
"""
from __future__ import annotations

import os
import typing
from dataclasses import dataclass
from pathlib import Path

from dbt.cli.main import dbtRunner, dbtRunnerResult

from sdk.entities.base.status import StatusState, build_status
from sdk.entities.dataitem.crud import get_dataitem, new_dataitem
from sdk.entities.run.crud import get_run, run_from_dict, update_run
from sdk.runtimes.objects.job.base import RuntimeJob
from sdk.utils.generic_utils import decode_string, encode_string, get_uiid

if typing.TYPE_CHECKING:
    from dbt.contracts.results import RunResult

    from sdk.entities.dataitem.entity import Dataitem
    from sdk.entities.run.entity import Run

####################
# ENV
####################
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA")

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


class RuntimeJobDBT(RuntimeJob):
    """
    Runtime job DBT class.
    """

    def __init__(self, spec: dict, run_id: str, project_name: str) -> None:
        """
        Constructor.

        See Also
        --------
        Runtime.__init__
        """
        super().__init__(spec, run_id, project_name)
        self.root_dir = Path("dbt_run")
        self.model_dir = self.root_dir / "models"
        self.dataitem_kind = "table"

    def job(self) -> Run:
        """
        Run function.

        Returns
        -------
        Run
            The executed run.
        """

        # Parse inputs/outputs
        inputs = self.parse_inputs()
        output = self.parse_outputs()

        # Setup environment
        uuid = get_uiid()
        self.setup(inputs, output, uuid)

        # Execute function
        execution_results = self.execute(output)

        # Parse results
        parsed_result = self.parse_results(execution_results, output)

        # Create dataitem
        dataitem = self.create_dataitem(parsed_result, uuid)

        # Update run
        return self.update_run_results(dataitem, parsed_result, output)

    ####################
    # Parse inputs/outputs
    ####################

    def parse_inputs(self) -> list:
        """
        Parse inputs from run spec.

        Returns
        -------
        list
            The list of inputs dataitems names.
        """
        inputs = self.spec.get("inputs", {}).get("dataitems", [])
        if not isinstance(inputs, list):
            self.handle_run_error("Inputs must be a list of dataitems")
        self.materialize_inputs(inputs)
        return inputs

    def materialize_inputs(self, inputs: list) -> None:
        """
        Materialize inputs in postgres.

        Parameters
        ----------
        inputs : list
            The list of inputs dataitems names.

        Returns
        -------
        None
        """
        for name in inputs:
            try:
                di = get_dataitem(self.project_name, name)
            except Exception:
                self.handle_run_error(
                    f"Dataitem {name} not found in project {self.project_name}"
                )
            target_path = (
                f"sql://postgres/{POSTGRES_DATABASE}/{POSTGRES_SCHEMA}/{name}_v{di.id}"
            )
            di.write_df(target_path, if_exists="replace")

    def parse_outputs(self) -> str:
        """
        Parse outputs from run spec.

        Returns
        -------
        str
            The output dataitem/table name.
        """
        outputs = self.spec.get("outputs", {}).get("dataitems", [])
        if not isinstance(outputs, list):
            self.handle_run_error("Outputs must be a list of dataitems")
        return outputs[0]

    ####################
    # Setup environment
    ####################

    def setup(self, inputs: list, output: str, uuid: str) -> None:
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

        Returns
        -------
        None
        """
        self.model_dir.mkdir(exist_ok=True, parents=True)

        # Generate profile yaml file
        self.generate_dbt_profile_yml()

        # Generate project yaml file
        self.generate_dbt_project_yml()

        # Generate outputs confs
        sql = self.decode_sql()
        self.generate_outputs_conf(sql, output, uuid)

        # Generate inputs confs
        self.generate_inputs_conf(inputs)

    def decode_sql(self) -> str:
        """
        Parse sql code.

        Returns
        -------
        str
            The decoded sql code.
        """
        return decode_string(self.spec.get("sql"))

    def generate_inputs_conf(self, inputs: list) -> None:
        """
        Generate inputs confs dependencies for dbt project.

        Parameters
        ----------
        inputs : list
            The list of inputs dataitems names.

        Returns
        -------
        None
        """
        for name in inputs:
            # Get dataitem from core
            response = get_dataitem(self.project_name, name)
            uuid = response.id

            # write schema and version detail for inputs versioning
            input_path = self.model_dir / f"{name}.sql"
            input_path.write_text(MODEL_TEMPLATE_UUID.format(name, uuid, uuid))

            # write also sql select for the schema
            sql_path = self.model_dir / f"{name}_v{uuid}.sql"
            sql_path.write_text(f'SELECT * FROM "{name}_v{uuid}"')

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
        sql_path = self.model_dir / f"{output}.sql"
        sql_path.write_text(sql)

        output_path = self.model_dir / f"{output}.yml"
        output_path.write_text(MODEL_TEMPLATE_VERSION.format(output, uuid, uuid))

    def generate_dbt_project_yml(self) -> None:
        """
        Create dbt_project.yml from 'dbt'

        Returns
        -------
        None
        """
        project_path = self.root_dir / "dbt_project.yml"
        project_path.write_text(
            PROJECT_TEMPLATE.format(
                self.project_name.replace("-", "_"), self.model_dir.name
            )
        )

    def generate_dbt_profile_yml(self) -> None:
        """
        Create dbt profiles.yml

        Returns
        -------
        None
        """
        profiles_path = self.root_dir / "profiles.yml"
        profiles_path.write_text(PROFILE_TEMPLATE)

    ####################
    # Execute function
    ####################

    def execute(self, output: str) -> dbtRunnerResult:
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

    def parse_results(self, run_result: dbtRunnerResult, output: str) -> ParsedResults:
        """
        Parse dbt results.

        Parameters
        ----------
        run_result : dbtRunnerResult
            The dbt result.
        output : str
            The output table name.

        Returns
        -------
        ParsedResults
            Parsed results.
        """
        result: RunResult = self.validate_results(run_result, output)
        try:
            path = self.get_path(result)
            raw_code = self.get_raw_code(result)
            compiled_code = self.get_compiled_code(result)
            timings = self.get_timings(result)
            name = result.node.name
        except Exception:
            self.handle_run_error("Something got wrong during results parsing.")
        return ParsedResults(name, path, raw_code, compiled_code, timings)

    def validate_results(self, run_result: dbtRunnerResult, output: str) -> RunResult:
        """
        Parse dbt results.

        Parameters
        ----------
        run_result : dbtRunnerResult
            The dbt result.
        output : str
            The output table name.

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
            self.handle_run_error("No results found.")

        if not result.status.value == "success":
            self.handle_run_error("Something got wrong during function execution.")

        if not result.node.package_name == self.project_name.replace("-", "_"):
            self.handle_run_error("Wrong project name.")

        if not result.node.name == output:
            self.handle_run_error("Wrong output name.")

        return result

    def get_path(self, result: RunResult) -> str:
        """
        Get path from dbt result (sql://postgres/database/schema/table).

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
        return f"sql://postgres/{components}"

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
        if compile_timing is None or execute_timing is None:
            raise
        if execute_timing.started_at is None or execute_timing.completed_at is None:
            raise
        if compile_timing.started_at is None or compile_timing.completed_at is None:
            raise
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

    def create_dataitem(self, result: ParsedResults, uuid: str) -> Dataitem | None:
        """
        Create new dataitem.

        Parameters
        ----------
        result : ParsedResults
            The parsed results.
        uuid : str
            The uuid of the model for outputs versioning.

        Returns
        -------
        Dataitem
            The dataitem.
        """
        try:
            return new_dataitem(
                project=self.project_name,
                name=result.name,
                kind=self.dataitem_kind,
                path=result.path,
                uuid=uuid,
                raw_code=result.raw_code,
                compiled_code=result.compiled_code,
            )
        except Exception:
            self.handle_run_error("Something got wrong during dataitem creation.")

    def get_dataitem_info(self, output: str, dataitem: Dataitem) -> dict:
        """
        Create dataitem info.

        Parameters
        ----------
        output : str
            The output table name.
        dataitem : Dataitem
            The dataitem.
        """
        return {
            "dataitems": [
                {
                    "key": output,
                    "kind": self.dataitem_kind,
                    "id": f"store://{dataitem.project}/dataitems/{dataitem.kind}/{dataitem.name}:{dataitem.id}",
                }
            ]
        }

    def update_run_results(
        self, dataitem: Dataitem, result: ParsedResults, output: str
    ) -> Run:
        """
        Update run with results infos.

        Parameters
        ----------
        dataitem : Dataitem
            The dataitem.
        result : ParsedResults
            The parsed results.
        output : str
            The output table name.

        Returns
        -------
        Run
            The updated run.

        Raises
        ------
        EntityError
            If something got wrong during run update.
        """

        status_dict = {
            **self.get_dataitem_info(output, dataitem),
            **result.timings,
            "state": StatusState.COMPLETED.value,
        }
        return self.update_run(**status_dict)

    def handle_run_error(self, msg: str) -> None:
        """
        Handle run error.

        Parameters
        ----------
        msg : str
            The error message.

        Returns
        -------
        None

        Raises
        ------
        RuntimeError
            Always.
        """
        self.update_run(state=StatusState.ERROR.value, error=msg)
        raise RuntimeError(msg)

    def update_run(self, **kwargs) -> Run:
        """
        Update run status.

        Parameters
        ----------
        **kwargs :
            Keyword arguments.

        Returns
        -------
        Run
            The updated run.

        Raises
        ------
        EntityError
            If something got wrong during run update.
        """
        run = get_run(self.project_name, self.run_id)
        run.set_status(build_status(**kwargs))
        new_run = update_run(run)
        return run_from_dict(new_run)
