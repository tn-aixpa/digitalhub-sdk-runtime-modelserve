from __future__ import annotations

from typing import Callable

func_registry = {}

try:
    from digitalhub_runtime_modelserve.utils.frameworks.sklearn import get_serve_function_sklearn

    func_registry["sklearnserve+serve"] = get_serve_function_sklearn
except ImportError:
    ...

try:
    from digitalhub_runtime_modelserve.utils.frameworks.mlflow import get_serve_function_mlflow

    func_registry["mlflowserve+serve"] = get_serve_function_mlflow
except ImportError:
    ...

try:
    from digitalhub_runtime_modelserve.utils.frameworks.huggingface import get_serve_function_huggingface

    func_registry["huggingfaceserve+serve"] = get_serve_function_huggingface

except ImportError:
    ...


def get_serve_function(action: str) -> Callable:
    """
    Get serve function.

    Parameters
    ----------
    action : str
        The action.

    Returns
    -------
    Callable
        The serve function.
    """
    return func_registry[action]
