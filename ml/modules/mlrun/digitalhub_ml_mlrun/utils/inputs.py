from __future__ import annotations

import typing

from digitalhub_core.entities.artifacts.crud import get_artifact
from digitalhub_core.utils.exceptions import BackendError
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


def get_inputs_parameters(spec: dict) -> dict:
    """
    Set inputs.

    Parameters
    ----------
    spec : dict
        Run spec.

    Returns
    -------
    dict
        Mlrun inputs.
    """
    inputs = spec.get("inputs", {})
    inputs_objects = {}
    for k, v in inputs.get("dataitems", {}):
        di: Dataitem = get_dataitem_(v)
        inputs_objects[k] = di.spec.path
    for k, v in inputs.get("artifacts", {}):
        ar: Artifact = get_artifact_(v)
        inputs_objects[k] = ar.spec.target_path
    return {
        "inputs": {
            **inputs_objects,
            **spec.get("parameters", {}).get("inputs", {}),
        },
    }
