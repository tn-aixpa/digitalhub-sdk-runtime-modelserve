from __future__ import annotations

import typing
from pathlib import Path

from digitalhub_core.entities.artifacts.crud import artifact_from_dict
from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.generic_utils import parse_entity_key
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data.entities.dataitems.crud import dataitem_from_dict

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity import Entity
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_data.entities.dataitems.entity._base import Dataitem
    from pandas import DataFrame

def persist_dataitem(dataitem: Dataitem, tmp_dir: Path) -> str:
    """
    Persist dataitem locally.

    Parameters
    ----------
    dataitem : Dataitem
        The dataitem to persist.
    tmp_dir : Path
        Temporary download directory.

    Returns
    -------
    str
        Temporary dataitem path.

    Raises
    ------
    EntityError
        If the dataitem cannot be persisted.
    """
    name = dataitem.name
    try:
        LOGGER.info(f"Persisting dataitem '{name}' locally.")
        tmp_path = tmp_dir / f"{name}.csv"
        dataframe: DataFrame = dataitem.as_df()
        dataframe.to_csv(tmp_path, sep=",", index=False)
        return str(tmp_path)
    except Exception:
        msg = f"Error during dataitem '{name}' collection."
        LOGGER.exception(msg)
        raise EntityError(msg)


def persist_artifact(artifact: Artifact, tmp_dir: Path) -> str:
    """
    Persist artifact locally.

    Parameters
    ----------
    artifact : Artifact
        The artifact object.
    tmp_dir : Path
        Temporary directory.

    Returns
    -------
    str
        Temporary artifact path.

    Raises
    ------
    EntityError
        If the artifact cannot be persisted.
    """
    name = artifact.name
    try:
        LOGGER.info(f"Persisting dataitem '{name}' locally.")
        filename = Path(artifact.spec.path).name
        dst = tmp_dir / filename
        tmp_path = artifact.download(dst=dst)
        return str(tmp_path)
    except Exception:
        msg = f"Error during artifact '{name}' collection."
        LOGGER.exception(msg)
        raise EntityError(msg)


def get_inputs_parameters(inputs: list[dict[str, Entity]], parameters: dict, tmp_dir: Path) -> dict:
    """
    Set inputs.

    Parameters
    ----------
    inputs : list[dict[str, Entity]]
        Run inputs.
    parameters : dict
        Run parameters.
    tmp_dir : Path
        Temporary directory for storing dataitms and artifacts.

    Returns
    -------
    dict
        Mlrun inputs.
    """
    inputs_objects = {}
    for i in inputs:
        for k, v in i.items():
            _, entity_type, _, _, _ = parse_entity_key(v.get("key"))
            if entity_type == "dataitems":
                v = dataitem_from_dict(v)
                inputs_objects[k] = persist_dataitem(v, tmp_dir)
            elif entity_type == "artifacts":
                v = artifact_from_dict(v)
                inputs_objects[k] = persist_artifact(v, tmp_dir)
    input_parameters = parameters.get("inputs", {})
    return {"inputs": {**inputs_objects, **input_parameters}}
