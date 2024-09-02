from __future__ import annotations

import os
import subprocess
from pathlib import Path

from digitalhub_core.utils.exceptions import EntityError
from digitalhub_core.utils.logger import LOGGER
from digitalhub_runtime_modelserve.utils.frameworks.utils import FILENAME, TEMPLATE

MLFLOW_RUNTIME = "mlserver_mlflow.MLflowRuntime"
ENDPOINT = "http://localhost:8080/v2/models/model/infer"


def serve_mlflow(root: Path) -> tuple:
    """
    Serve mlflow function.

    Parameters
    ----------
    root : Path
        The root path where config file is.

    Returns
    -------
    tuple
        Process ID and serving endpoint.
    """
    try:
        current_dir = os.getcwd()
        os.chdir(root)
        proc = subprocess.Popen(["mlserver", "start", "."])
        pid = proc.pid
        os.chdir(current_dir)
        return pid, ENDPOINT
    except Exception as e:
        msg = f"Something got wrong during mlflow serving. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise EntityError(msg) from e


def config_mlflow(root: Path, paths: list) -> None:
    """
    Configure mlflow function.

    Parameters
    ----------
    root : Path
        The root path where config file is.
    paths : list
        List of paths.

    Returns
    -------
    None
    """
    model_path = None
    for p in paths:
        p = p.removeprefix(str(root) + "/")
        if "best_estimator/MLmodel" in p:
            model_path = p.removesuffix("MLmodel")
            break
        elif "model/MLmodel" in p:
            model_path = p.removesuffix("MLmodel")
            break
    if model_path is None:
        raise Exception("MLflow model not found")

    serving_json = TEMPLATE.format(MLFLOW_RUNTIME, model_path)
    (root / FILENAME).write_text(serving_json)
