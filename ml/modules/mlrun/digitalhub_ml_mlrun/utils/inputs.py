from __future__ import annotations

import typing
from pathlib import Path

from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.logger import LOGGER

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_data.entities.dataitems.entity._base import Dataitem


def persist_dataitem(dataitem: Dataitem, name: str, tmp_dir: str) -> str:
    """
    Persist dataitem locally.

    Parameters
    ----------
    dataitem : Dataitem
        The dataitem to persist.
    name : str
        The dataitem name.
    tmp_dir : str
        Temporary download directory.

    Returns
    -------
    str
        The dataitem path.

    Raises
    ------
    EntityError
        If the dataitem cannot be persisted.
    """
    try:
        LOGGER.info(f"Persisting dataitem '{name}' locally.")
        tmp_path = f"{tmp_dir}/{name}.csv"
        dataitem.as_df().to_csv(tmp_path, sep=",", index=False)
        return tmp_path
    except Exception:
        msg = f"Error during dataitem '{name}' collection."
        LOGGER.exception(msg)
        raise EntityError(msg)


def persist_artifact(artifact: Artifact, name: str, tmp_dir: str) -> str:
    """
    Persist artifact locally.

    Parameters
    ----------
    artifact : Artifact
        The artifact object.
    name : str
        The artifact name.
    tmp_dir : str
        Temporary directory.

    Returns
    -------
    str
        The artifact path.

    Raises
    ------
    EntityError
        If the artifact cannot be persisted.
    """
    try:
        LOGGER.info(f"Persisting dataitem '{name}' locally.")
        filename = Path(artifact.spec.path).name
        return artifact.download(dst=f"{tmp_dir}/{filename}")
    except Exception:
        msg = f"Error during artifact '{name}' collection."
        LOGGER.exception(msg)
        raise EntityError(msg)


def get_inputs_parameters(inputs: dict, parameters: dict, project: str, tmp_dir: str) -> dict:
    """
    Set inputs.

    Parameters
    ----------
    inputs : dict
        Run inputs.
    parameters : dict
        Run parameters.
    project : str
        The project name.
    tmp_dir : str
        Temporary directory for storing dataitms and artifacts.

    Returns
    -------
    dict
        Mlrun inputs.
    """
    inputs_objects = {}
    k = 0
    for di in inputs["dataitems"]:
        inputs_objects[k] = persist_dataitem(di, di.name, tmp_dir)
        k += 1

    k = 0
    for ar in inputs["artifacts"]:
        inputs_objects[k] = persist_artifact(ar, ar.name, tmp_dir)
        k += 1

    input_parameters = parameters.get("inputs", {})
    return {"inputs": {**inputs_objects, **input_parameters}}
