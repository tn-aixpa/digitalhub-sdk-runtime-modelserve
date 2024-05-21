from __future__ import annotations

import pickle
import typing
from typing import Any

import pandas as pd
from digitalhub_core.entities._base.status import State
from digitalhub_core.entities.artifacts.crud import new_artifact
from digitalhub_core.utils.logger import LOGGER
from digitalhub_data.entities.dataitems.crud import new_dataitem

if typing.TYPE_CHECKING:
    from digitalhub_data.entities.dataitems.entity.table import DataitemTable


def collect_outputs(results: Any, outputs: list[str], project_name: str) -> dict:
    """
    Collect outputs. Use the produced results directly.

    Parameters
    ----------
    results : Any
        Function outputs.
    project : Project
        Project object.

    Returns
    -------
    dict
        Function outputs.
    """
    objects = {}
    results = listify_results(results)

    for idx, item in enumerate(results):
        try:
            name = outputs[idx]
        except IndexError:
            name = f"output_{idx}"

        if isinstance(item, pd.DataFrame):
            objects[name] = build_and_load_dataitem(name, project_name, item)

        elif isinstance(item, (str, int, float, bool, bytes)):
            objects[name] = item

        else:
            objects[name] = build_and_load_artifact(name, project_name, item)

    return objects


def listify_results(results: Any) -> list:
    """
    Listify results.

    Parameters
    ----------
    results : Any
        Function outputs.

    Returns
    -------
    list
        Function outputs.
    """
    if results is None:
        return []

    if not isinstance(results, (tuple, list)):
        results = [results]

    return results


def build_and_load_dataitem(name: str, project_name: str, data: Any) -> str:
    """
    Build and load dataitem.

    Parameters
    ----------
    name : str
        Dataitem name.
    project_name : str
        Project name.
    data : Any
        Data.

    Returns
    -------
    str
        Dataitem key.
    """
    try:
        path = f"s3://datalake/{project_name}/dataitems/table/{name}.parquet"
        di: DataitemTable = new_dataitem(project=project_name, name=name, kind="table", path=path)
        di.write_df(df=data)
        return di.key
    except Exception as e:
        msg = f"Some error occurred while building and loading dataitem. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def build_and_load_artifact(name: str, project_name: str, data: Any) -> str:
    """
    Build and load artifact.

    Parameters
    ----------
    name : str
        Artifact name.
    project_name : str
        Project name.
    data : Any
        Data.

    Returns
    -------
    str
        Artifact key.
    """
    try:
        path = f"s3://datalake/{project_name}/artifacts/artifact/{name}.pickle"

        # Dump item to pickle
        with open(f"{name}.pickle", "wb") as f:
            f.write(pickle.dumps(data))

        art = new_artifact(project=project_name, name=name, kind="artifact", path=path)
        art.upload(source=f"{name}.pickle")
        return art.key

    except Exception as e:
        msg = f"Some error occurred while building and loading artifact. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def build_status(outputs: dict) -> dict:
    """
    Build status from outputs.

    Parameters
    ----------
    outputs : dict
        Function outputs.

    Returns
    -------
    dict
        Function status.
    """
    try:
        return {
            "state": State.COMPLETED.value,
            "outputs": outputs,
        }
    except Exception as e:
        msg = f"Some error occurred while building status. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg)
