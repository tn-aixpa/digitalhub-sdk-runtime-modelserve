from __future__ import annotations

import typing

from digitalhub_core.entities._base.status import State
from digitalhub_core.entities.artifacts.crud import new_artifact
from digitalhub_core.runtimes.results import get_entity_info
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data.entities.dataitems.crud import create_dataitem
from digitalhub_data.utils.data_utils import get_data_preview

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_data.entities.dataitems.entity import Dataitem


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
        "completed": State.COMPLETED.value,
        "error": State.ERROR.value,
        "running": State.RUNNING.value,
        "created": State.CREATED.value,
        "pending": State.PENDING.value,
        "unknown": State.ERROR.value,
        "aborted": State.STOP.value,
        "aborting": State.STOP.value,
    }
    return kfp_states.get(state, State.ERROR.value)


def parse_kfp_artifacts(kfp_outputs: list[dict]) -> list[Artifact]:
    """
    Filter out results from KFP outputs and create DHCore artifacts.

    Parameters
    ----------
    kfp_outputs : list[dict]
        KFP outputs.

    Returns
    -------
    list[Artifact]
        DHCore artifacts list.
    """
    outputs = []
    for i in kfp_outputs:
        if i.get("kind") == "model":
            ...
        elif i.get("kind") == "dataset":
            outputs.append(create_dataitem_(i))
        else:
            outputs.append(create_artifact(i))
    return outputs


def create_artifact(kfp_artifact: dict) -> Artifact:
    """
    New artifact.

    Parameters
    ----------
    kfp_artifact : dict
        KFP artifact.

    Returns
    -------
    dict
        Artifact info.
    """
    try:
        kwargs = {}
        kwargs["project"] = kfp_artifact.get("metadata", {}).get("project")
        kwargs["name"] = kfp_artifact.get("metadata", {}).get("key")
        kwargs["kind"] = "artifact"
        kwargs["target_path"] = kfp_artifact.get("spec", {}).get("target_path")
        kwargs["size"] = kfp_artifact.get("spec", {}).get("size")
        kwargs["hash"] = kfp_artifact.get("spec", {}).get("hash")
        return new_artifact(**kwargs)
    except Exception:
        msg = "Something got wrong during artifact creation."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def create_dataitem_(kfp_output: dict) -> Dataitem:
    """
    New dataitem.

    Parameters
    ----------
    kfp_output : dict
        KFP output.

    Returns
    -------
    dict
        Dataitem info.
    """
    try:
        # Create dataitem
        kwargs = {}
        kwargs["project"] = kfp_output.get("metadata", {}).get("project")
        kwargs["name"] = kfp_output.get("metadata", {}).get("key")
        kwargs["kind"] = "dataitem"
        kwargs["path"] = kfp_output.get("spec", {}).get("target_path")
        kwargs["schema"] = kfp_output.get("spec", {}).get("schema", {}).get("fields")
        dataitem = create_dataitem(**kwargs)

        # Add sample preview
        header = kfp_output.get("spec", {}).get("header", [])
        sample_data = kfp_output.get("status", {}).get("preview", [[]])
        dataitem.status.preview = _get_data_preview(header, sample_data)

        # Save dataitem in core and return it
        dataitem.save()
        return dataitem
    except Exception:
        msg = "Something got wrong during dataitem creation."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def _get_data_preview(columns: tuple, data: list[tuple]) -> list[dict]:
    """
    Get data preview from KFP result.

    Parameters
    ----------
    columns : tuple
        The columns.
    data : list[tuple]
        The data.

    Returns
    -------
    list
        A list of dictionaries containing data.
    """
    try:
        return get_data_preview(columns, data)
    except Exception:
        msg = "Something got wrong during data preview creation."
        LOGGER.exception(msg)
        raise RuntimeError(msg)


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
                artifacts.append(get_entity_info(i, "artifacts"))
            elif i.__class__.__name__ == "Dataitem":
                dataitems.append(get_entity_info(i, "dataitems"))
        return {
            "state": map_state(execution_results.status.state),
            "outputs": {
                "artifacts": artifacts,
                "dataitems": dataitems,
            },
            "results": execution_results.to_json(),
        }
    except Exception:
        msg = "Something got wrong during run status building."
        LOGGER.exception(msg)
        raise RuntimeError(msg)