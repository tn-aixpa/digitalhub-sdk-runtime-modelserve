from __future__ import annotations

import json
import typing
from datetime import datetime

from digitalhub_core.entities._base.status import State
from digitalhub_core.utils.logger import LOGGER

if typing.TYPE_CHECKING:
    from kfp_server_api.models import ApiRun, ApiRunDetail


def map_state(state: str) -> str:
    """
    Map KFP state to digitalhub state.

    Parameters
    ----------
    state : str
        KFP state.

    Returns
    -------
    str
        Mapped digitalhub state.
    """
    kfp_states = {
        "Succeeded": State.COMPLETED.value,
        "Failed": State.ERROR.value,
        "Running": State.RUNNING.value,
        "Pending": State.PENDING.value,
        "Skipped": State.STOP.value,
        "Error": State.ERROR.value,
    }
    return kfp_states.get(state, State.ERROR.value)


def build_status(execution_results: ApiRunDetail, outputs: list[dict] = None, values: list[str] = None) -> dict:
    """
    Collect outputs.

    Parameters
    ----------
    execution_results : ApiRun
        KFP Execution results.
    outputs : list[dict]
        List of entities to map the outputs to.
    values : list[str]
        List of simple values to map the outputs to.

    """
    try:
        run = execution_results.run
        return {
            "state": map_state(run.status),
            "results": _convert_run(run),
        }
    except Exception:
        msg = "Something got wrong during run status building."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def _convert_run(run: ApiRun) -> dict:
    """
    Convert run to dict.

    Parameters
    ----------
    run : ApiRun
        KFP run.

    Returns
    -------
    dict
        Run dict.
    """
    try:
        dict = run.to_dict()
        return json.loads(json.dumps(dict, cls=DateTimeEncoder))
    except Exception:
        msg = "Something got wrong during run conversion."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)
