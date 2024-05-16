from __future__ import annotations

import pickle
import typing
from typing import Any

import pandas as pd
from digitalhub_data.entities.dataitems.crud import new_dataitem
from digitalhub_core.entities.artifacts.crud import new_artifact

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
    if results is None:
        return {}

    if not isinstance(results, (tuple, list)):
        results = [results]

    objects = {}

    for idx, item in enumerate(results):
        try:
            name = outputs[idx]
        except IndexError:
            name = f"output_{idx}"

        if isinstance(item, pd.DataFrame):
            path = f"s3://datalake/{project_name}/dataitems/table/{name}.parquet"
            di: DataitemTable = new_dataitem(project=project_name,
                                             name=name,
                                             kind="table",
                                             path=path)
            di.write_df(df=item)
            objects[name] = di.key

        elif isinstance(item, (str, int, float, bool, bytes)):
            objects[name] = item

        else:
            path = f"s3://datalake/{project_name}/artifacts/artifact/{name}.pickle"

            # Dump item to pickle
            with open(f"{name}.pickle", "wb") as f:
                f.write(pickle.dumps(item))

            art = new_artifact(project=project_name,
                               name=name,
                               kind="artifact",
                               path=path)
            art.upload(source=f"{name}.pickle")
            objects[name] = art.key

    return objects
