"""
Runtime DBT parsing utils module.
"""
from __future__ import annotations

import typing
from dataclasses import dataclass

from dbt.cli.main import dbtRunnerResult
from digitalhub_core.utils.generic_utils import encode_string
from digitalhub_core.utils.logger import LOGGER

if typing.TYPE_CHECKING:
    from dbt.contracts.results import RunResult


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


def parse_results(run_result: dbtRunnerResult, output: str, project: str) -> ParsedResults:
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
    result: RunResult = validate_results(run_result, output, project)
    try:
        path = get_path(result)
        raw_code = get_raw_code(result)
        compiled_code = get_compiled_code(result)
        timings = get_timings(result)
        name = result.node.name
        return ParsedResults(name, path, raw_code, compiled_code, timings)
    except Exception:
        msg = "Something got wrong during results parsing."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def validate_results(run_result: dbtRunnerResult, output: str, project: str) -> RunResult:
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


def get_path(result: RunResult) -> str:
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
    try:
        components = result.node.relation_name.replace('"', "")
        components = "/".join(components.split("."))
        return f"sql://{components}"
    except Exception:
        msg = "Something got wrong during path parsing."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def get_raw_code(result: RunResult) -> str:
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
    try:
        return encode_string(str(result.node.raw_code))
    except Exception:
        msg = "Something got wrong during raw code parsing."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def get_compiled_code(result: RunResult) -> str:
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
    try:
        return encode_string(str(result.node.compiled_code))
    except Exception:
        msg = "Something got wrong during compiled code parsing."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def get_timings(result: RunResult) -> dict:
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
    try:
        compile_timing = None
        execute_timing = None
        for entry in result.timing:
            if entry.name == "compile":
                compile_timing = entry
            elif entry.name == "execute":
                execute_timing = entry
        return {
            "compile": {
                "started_at": compile_timing.started_at.isoformat(),
                "completed_at": compile_timing.completed_at.isoformat(),
            },
            "execute": {
                "started_at": execute_timing.started_at.isoformat(),
                "completed_at": execute_timing.completed_at.isoformat(),
            },
        }
    except Exception:
        msg = "Something got wrong during timings parsing."
        LOGGER.exception(msg)
        raise RuntimeError(msg)
