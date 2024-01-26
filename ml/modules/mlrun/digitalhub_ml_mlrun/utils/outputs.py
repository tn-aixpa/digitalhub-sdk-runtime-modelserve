from __future__ import annotations

import typing

import numpy as np
from digitalhub_core.entities._base.status import State
from digitalhub_core.entities.artifacts.crud import new_artifact
from digitalhub_core.entities.artifacts.utils import get_artifact_info
from digitalhub_core.entities.dataitems.crud import create_dataitem
from digitalhub_core.entities.dataitems.utils import get_dataitem_info
from digitalhub_core.utils.logger import LOGGER
from pandas import isna

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_core.entities.dataitems.entity import Dataitem
    from mlrun.runtimes.base import RunObject


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


def parse_mlrun_artifacts(mlrun_outputs: list[dict]) -> list[Artifact]:
    """
    Filter out models and datasets from MLRun outputs and create DHCore artifacts.

    Parameters
    ----------
    mlrun_outputs : list[dict]
        MLRun outputs.

    Returns
    -------
    list[Artifact]
        DHCore artifacts list.
    """
    outputs = []
    for i in mlrun_outputs:
        if i.get("kind") == "model":
            ...
        elif i.get("kind") == "dataset":
            outputs.append(create_dataitem_(i))
        else:
            outputs.append(create_artifact(i))
    return outputs


def create_artifact(mlrun_artifact: dict) -> Artifact:
    """
    New artifact.

    Parameters
    ----------
    mlrun_artifact : dict
        Mlrun artifact.

    Returns
    -------
    dict
        Artifact info.
    """
    try:
        kwargs = {}
        kwargs["project"] = mlrun_artifact.get("metadata", {}).get("project")
        kwargs["name"] = mlrun_artifact.get("metadata", {}).get("key")
        kwargs["kind"] = "artifact"
        kwargs["target_path"] = mlrun_artifact.get("spec", {}).get("target_path")
        kwargs["size"] = mlrun_artifact.get("spec", {}).get("size")
        kwargs["hash"] = mlrun_artifact.get("spec", {}).get("hash")
        return new_artifact(**kwargs)
    except Exception:
        msg = "Something got wrong during artifact creation."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def create_dataitem_(mlrun_output: dict) -> Dataitem:
    """
    New dataitem.

    Parameters
    ----------
    mlrun_output : dict
        Mlrun output.

    Returns
    -------
    dict
        Dataitem info.
    """
    try:
        # Create dataitem
        kwargs = {}
        kwargs["project"] = mlrun_output.get("metadata", {}).get("project")
        kwargs["name"] = mlrun_output.get("metadata", {}).get("key")
        kwargs["kind"] = "dataitem"
        kwargs["path"] = mlrun_output.get("spec", {}).get("target_path")
        kwargs["schema"] = mlrun_output.get("spec", {}).get("schema", {}).get("fields")
        dataitem = create_dataitem(**kwargs)

        # Add sample preview
        header = mlrun_output.get("spec", {}).get("header", [])
        sample_data = mlrun_output.get("status", {}).get("preview", [[]])
        dataitem.status.preview = pivot_preview(header, sample_data)

        # Save dataitem in core and return it
        dataitem.save()
        return dataitem
    except Exception:
        msg = "Something got wrong during dataitem creation."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def pivot_preview(columns: list, data: list[list]) -> list[list]:
    """
    Pivot preview from MLRun.

    Parameters
    ----------
    columns : list
        Columns.
    data : list[list]
        Data preview.

    Returns
    -------
    list[list]
        Pivoted preview.
    """
    ordered_data = np.array(data).T
    ordered_data = np.where(isna(ordered_data), None, ordered_data)
    ordered_data = np.where(isinstance(ordered_data, memoryview), None, ordered_data)
    ordered_data = ordered_data.tolist()
    return [{"name": c, "value": d} for c, d in zip(columns, ordered_data)]


def build_status(execution_results: RunObject, outputs: list[Artifact | Dataitem]) -> dict:
    """
    Collect outputs.

    Parameters
    ----------
    execution_results : RunObject
        Execution results.
    outputs : list[Artifact | Dataitem]
        List of entities to collect outputs from.

    """
    try:
        artifacts = []
        dataitems = []
        for i in outputs:
            if i.__class__.__name__ == "Artifact":
                artifacts.append(get_artifact_info(i))
            elif i.__class__.__name__ == "Dataitem":
                dataitems.append(get_dataitem_info(i))
        return {
            "state": map_state(execution_results.status.state),
            "artifacts": artifacts,
            "dataitems": dataitems,
            "timings": {
                "start": execution_results.status.start_time,
                "updated": execution_results.status.last_update,
            },
            "mlrun_results": execution_results.to_json(),
        }
    except Exception:
        msg = "Something got wrong during run status building."
        LOGGER.exception(msg)
        raise RuntimeError(msg)
