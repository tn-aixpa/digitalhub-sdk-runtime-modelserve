from __future__ import annotations

import typing
from pathlib import Path

from digitalhub_core.entities.artifacts.crud import get_artifact
from digitalhub_core.utils.exceptions import BackendError, EntityError
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data.entities.dataitems.crud import get_dataitem

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_data.entities.dataitems.entity import Dataitem


def get_dataitem_(name: str, project: str) -> Dataitem:
    """
    Get dataitem from core.

    Parameters
    ----------
    name : str
        The dataitem name.
    project : str
        The project name.

    Returns
    -------
    Dataitem
        The dataitem.

    Raises
    ------
    BackendError
        If dataitem is not found.
    """
    try:
        LOGGER.info(f"Getting dataitem '{name}'")
        return get_dataitem(project, name)
    except BackendError:
        msg = f"Dataitem {name} not found."
        LOGGER.exception(msg)
        raise BackendError(msg)


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


def get_artifact_(name: str, project: str) -> Artifact:
    """
    Get artifact from core.

    Parameters
    ----------
    name : str
        The artifact name.
    project : str
        The project name.

    Returns
    -------
    dict
        The artifact.

    Raises
    ------
    BackendError
        If artifact is not found.
    """
    try:
        LOGGER.info(f"Getting artifact '{name}'")
        return get_artifact(project, name)
    except BackendError:
        msg = f"Artifact {name} not found."
        LOGGER.exception(msg)
        raise BackendError(msg)


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
        filename = Path(artifact.spec.target_path).name
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
    for k, v in inputs.get("dataitems", {}).items():
        di: Dataitem = get_dataitem_(v, project)
        inputs_objects[k] = persist_dataitem(di, v, tmp_dir)
    for k, v in inputs.get("artifacts", {}).items():
        ar: Artifact = get_artifact_(v, project)
        inputs_objects[k] = persist_artifact(ar, v, tmp_dir)
    input_parameters = parameters.get("inputs", {})
    return {"inputs": {**inputs_objects, **input_parameters}}
