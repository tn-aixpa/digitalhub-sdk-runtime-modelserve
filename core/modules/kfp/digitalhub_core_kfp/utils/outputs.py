from __future__ import annotations

import typing

from digitalhub_core.entities._base.status import State
from digitalhub_core.entities.artifacts.crud import new_artifact
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data.entities.dataitems.crud import create_dataitem
from digitalhub_data.utils.data_utils import get_data_preview

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_data.entities.dataitems.entity import Dataitem
    from kfp_server_api.models import ApiRunDetail


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
            "state": map_state(run.status.state),
            "results": run.to_json(),
        }
    except Exception:
        msg = "Something got wrong during run status building."
        LOGGER.exception(msg)
        raise RuntimeError(msg)