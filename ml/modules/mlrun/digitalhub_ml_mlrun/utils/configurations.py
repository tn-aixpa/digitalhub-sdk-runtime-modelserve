from __future__ import annotations

import typing

from digitalhub_core.entities._base.status import State
from digitalhub_core.utils.logger import LOGGER
from mlrun import get_or_create_project

if typing.TYPE_CHECKING:
    from mlrun.projects import MlrunProject
    from mlrun.runtimes import BaseRuntime


####################
# Configuration
####################


def get_mlrun_project(project_name: str) -> MlrunProject:
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
    try:
        return get_or_create_project(project_name, "./")
    except Exception:
        msg = f"Error getting MLRun project '{project_name}'."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def get_mlrun_function(
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
    try:
        project.set_function(function_source, name=function_name, **function_specs)
        project.save()
        return project.get_function(function_name)
    except Exception:
        msg = f"Error getting MLRun function '{function_name}'."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


####################
# Output
####################


def map_state(state: str) -> str:
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
    mlrun_states = {
        "completed": State.COMPLETED.value,
        "error": State.ERROR.value,
        "running": State.RUNNING.value,
        "created": State.CREATED.value,
        "pending": State.PENDING.value,
        "unknown": State.ERROR.value,
        "aborted": State.STOP.value,
        "aborting": State.STOP.value,
    }
    return mlrun_states.get(state, State.ERROR.value)
