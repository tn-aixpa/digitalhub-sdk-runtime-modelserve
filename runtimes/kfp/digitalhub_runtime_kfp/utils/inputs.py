from __future__ import annotations

import typing
from pathlib import Path

from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.logger import LOGGER

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity import Entity
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_data.entities.dataitems.entity.table import DataitemTable


def persist_dataitem(dataitem: DataitemTable, name: str, tmp_dir: str) -> str:
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
        dataitem.write_df(tmp_path, extension="csv", sep=",", index=False)
        return tmp_path
    except Exception as e:
        msg = f"Error during dataitem '{name}' collection. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise EntityError(msg) from e


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
    except Exception as e:
        msg = f"Error during artifact '{name}' collection. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise EntityError(msg) from e


def get_inputs_parameters(inputs: dict[str, Entity], parameters: dict) -> dict:
    """
    Set inputs.

    Parameters
    ----------
    inputs : dict[str, Entity]
        Run inputs.
    parameters : dict
        Run parameters.
    tmp_dir : str
        Temporary directory for storing dataitms and artifacts.

    Returns
    -------
    dict
        Mlrun inputs.
    """
    inputs_objects = {}
    for k, v in inputs.items():
        inputs_objects[k] = v
    input_parameters = parameters if parameters is not None else {}
    return {**inputs_objects, **input_parameters}
