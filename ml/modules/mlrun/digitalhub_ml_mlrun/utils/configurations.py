from __future__ import annotations

import typing

from digitalhub_core.entities.functions.crud import get_function
from digitalhub_core.utils.generic_utils import build_uuid, decode_string
from digitalhub_core.utils.logger import LOGGER
from mlrun import get_or_create_project

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.functions.entity import Function
    from digitalhub_ml_mlrun.entities.functions.spec import FunctionSpecMlrun
    from mlrun.projects import MlrunProject
    from mlrun.runtimes import BaseRuntime


def get_dhcore_function(function_string: str) -> Function:
    """
    Get DHCore function.

    Parameters
    ----------
    function_string : str
        Function string.

    Returns
    -------
    Function
        DHCore function.
    """
    splitted = function_string.split("://")[1].split("/")
    function_name, function_version = splitted[1].split(":")
    LOGGER.info(f"Getting function {function_name}:{function_version}.")
    try:
        return get_function(splitted[0], function_name, function_version)
    except Exception:
        msg = f"Error getting function {function_name}:{function_version}."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def save_function_source(path: str, spec: FunctionSpecMlrun) -> str:
    """
    Save function source.

    Parameters
    ----------
    path : str
        Path to the function source.
    function : FunctionSpecMlrun
        DHCore function spec.

    Returns
    -------
    path
        Path to the function source.
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
        filename = build_uuid().replace("-", "_") + ".py"
        path = path / filename
        decoded_text = decode_string(spec.build.source_encoded)
        path.write_text(decoded_text)
        return str(path)
    except Exception:
        msg = "Error saving function source."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def get_mlrun_project(project_name: str) -> MlrunProject:
    """
    Get Mlrun project.

    Parameters
    ----------
    project_name : str
        Project name.

    Returns
    -------
    MlrunProject
        Mlrun project.
    """
    try:
        return get_or_create_project(project_name, "./")
    except Exception:
        msg = f"Error getting Mlrun project '{project_name}'."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def get_mlrun_function(
    project: MlrunProject,
    function_name: str,
    function_source: str,
    function_specs: dict,
) -> BaseRuntime:
    """
    Get Mlrun function.

    Parameters
    ----------
    project : MlrunProject
        Mlrun project.
    function_name : str
        Name of the function.
    function_source : str
        Path to the function source.
    function_specs : dict
        Function specs.

    Returns
    -------
    BaseRuntime
        Mlrun function.
    """
    try:
        project.set_function(function_source, name=function_name, **function_specs)
        project.save()
        return project.get_function(function_name)
    except Exception:
        msg = f"Error getting Mlrun function '{function_name}'."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def parse_function_specs(spec: FunctionSpecMlrun) -> dict:
    """
    Parse function specs.

    Parameters
    ----------
    function : FunctionSpecMlrun
        DHCore function spec.

    Returns
    -------
    dict
        Function specs.
    """
    try:
        return {
            "image": spec.image,
            "tag": spec.tag,
            "handler": spec.handler,
            "requirements": spec.requirements,
        }
    except AttributeError:
        msg = "Error parsing function specs."
        LOGGER.error(msg)
        raise RuntimeError(msg)
