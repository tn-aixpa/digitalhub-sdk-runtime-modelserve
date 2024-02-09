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


def get_inputs_parameters(inputs: dict, parameters: dict, project: str) -> dict:
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

    Returns
    -------
    dict
        Mlrun inputs.
    """
    inputs_objects = {}
    for k, v in inputs.get("dataitems", {}).items():
        di: Dataitem = get_dataitem_(v, project)
        inputs_objects[k] = di.spec.path
    for k, v in inputs.get("artifacts", {}).items():
        ar: Artifact = get_artifact_(v, project)
        inputs_objects[k] = ar.spec.target_path
    input_parameters = parameters.get("inputs", {})
    return {"inputs": {**inputs_objects, **input_parameters}}
