from __future__ import annotations

from digitalhub_runtime_modelserve.utils.frameworks.registry import config_function_registry


def get_function_args(action: str, spec: dict, model_path: str) -> dict:
    """
    Get function arguments.

    Parameters
    ----------
    action : str
        The action.
    spec : dict
        The run spec.

    Returns
    -------
    dict
        The function arguments.
    """
    return config_function_registry[action](spec, model_path)
