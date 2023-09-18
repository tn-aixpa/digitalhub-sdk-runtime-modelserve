"""
DBT Runtime module.
"""
from __future__ import annotations

import os
import typing
from dataclasses import dataclass
from pathlib import Path

from dbt.cli.main import dbtRunner, dbtRunnerResult

from sdk.entities.dataitem.crud import get_dataitem, new_dataitem
from sdk.entities.run.crud import get_run, update_run, run_from_dict
from sdk.runtimes.objects.base import Runtime
from sdk.utils.exceptions import EntityError
from sdk.utils.generic_utils import decode_string, encode_string, get_uiid

if typing.TYPE_CHECKING:
    from dbt.contracts.results import RunResult

    from sdk.entities.dataitem.entity import Dataitem
    from sdk.entities.run.entity import Run


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
            host: {os.getenv("POSTGRES_HOST")}
            user: {os.getenv("POSTGRES_USER")}
            pass: {os.getenv("POSTGRES_PASSWORD")}
            port: {os.getenv("POSTGRES_PORT")}
            dbname: {os.getenv("POSTGRES_DB")}
            schema: public
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


class DBTRuntime(Runtime):
    """
    DBT Runtime class.
    """

    def __init__(
        self,
        spec: dict,
        run_id: str,
        project_name: str,
    ) -> None:
        """
        Constructor.

        See Also
        --------
        Runtime.__init__
        """
        super().__init__(spec, run_id, project_name)
        self.model_dir = Path("models")
        self.dataitem_kind = "table"

    def run(self) -> Run:
        """
        Run function.

        Returns
        -------
        Run
            The updated run.
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
        return self.update_run(parsed_result, output, dataitem)

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

        Raises
        ------
        EntityError
            If inputs are not a list of dataitems.
        """
        inputs = self.spec.get("inputs", {}).get("dataitems", [])
        if not isinstance(inputs, list):
            raise EntityError("Inputs must be a list of dataitems")
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

        Raises
        ------
        EntityError
            If dataitem is not found.
        """
        for name in inputs:
            try:
                di = get_dataitem(self.project_name, name)
            except Exception:
                raise EntityError(
                    f"Dataitem {name} not found in project {self.project_name}"
                )
            df = di.as_df()
            db = os.getenv("POSTGRES_DB")
            schema = os.getenv("POSTGRES_SCHEMA")
            target_path = f"sql://postgres/{db}/{schema}/{name}_v{di.id}"
            di.write_df(df, target_path, if_exists="replace")

    def parse_outputs(self) -> str:
        """
        Parse outputs from run spec.

        Returns
        -------
        str
            The output dataitem/table name.

        Raises
        ------
        EntityError
            If outputs are not a list of dataitems.
        """
        outputs = self.spec.get("outputs", {}).get("dataitems", [])
        if not isinstance(outputs, list):
            raise EntityError("Outputs must be a list of dataitems")
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
        # to clean project add clean-targets: [target, dbt_packages, logs]
        Path("dbt_project.yml").write_text(
            PROJECT_TEMPLATE.format(self.project_name.replace("-", "_"), self.model_dir)
        )

    def generate_dbt_profile_yml(self) -> None:
        """
        Create dbt profiles.yml

        Returns
        -------
        None
        """
        Path("profiles.yml").write_text(PROFILE_TEMPLATE)

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
        dbt = dbtRunner()
        dbt.invoke("clean")
        cli_args = ["run", "--select", f"{output}"]
        return dbt.invoke(cli_args)

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

        Raises
        ------
        RuntimeError
            If something got wrong during object result access.
        """
        result: RunResult = self.validate_results(run_result, output)
        try:
            path = self.get_path(result)
            raw_code, compiled_code = self.get_code(result)
            timings = self.get_timings(result)
            name = result.node.name
        except Exception as e:
            raise RuntimeError("Something got wrong during object result access") from e
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
        """
        # Take last result, final result of the query
        try:
            result: RunResult = run_result.result[-1]
        except IndexError:
            raise RuntimeError("No results found.")

        if not result.status.value == "success":
            raise RuntimeError("Execution is not successfull.")

        if not result.node.package_name == self.project_name.replace("-", "_"):
            raise RuntimeError("Wrong project name.")

        if not result.node.name == output:
            raise RuntimeError("Wrong function name.")

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

    def get_code(self, result: RunResult) -> tuple:
        """
        Get code from dbt result.

        Parameters
        ----------
        result : RunResult
            The dbt result.

        Returns
        -------
        tuple
            A tuple containing raw and compiled code.
        """
        raw_code = encode_string(result.node.raw_code)
        compiled_code = encode_string(result.node.compiled_code)
        return raw_code, compiled_code

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

    def create_dataitem(self, result: ParsedResults, uuid: str) -> Dataitem:
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

        Raises
        ------
        EntityError
            If something got wrong during dataitem creation.
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
        except Exception as e:
            raise EntityError("Something got wrong during dataitem creation") from e

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

    def update_run(self, result: ParsedResults, output: str, dataitem: Dataitem) -> Run:
        """
        Update run with results infos.

        Parameters
        ----------
        result : ParsedResults
            The parsed results.
        output : str
            The output table name.
        dataitem : Dataitem
            The new created dataitem.

        Returns
        -------
        Run
            The updated run.

        Raises
        ------
        EntityError
            If something got wrong during run update.
        """
        dataitem_info = self.get_dataitem_info(output, dataitem)
        status_dict = {
            **dataitem_info,
            **result.timings,
        }
        run = get_run(self.project_name, self.run_id)
        run.set_status(status_dict)
        try:
            updated = update_run(run)
        except Exception as e:
            raise EntityError("Something got wrong during run update") from e
        return run_from_dict(updated)
