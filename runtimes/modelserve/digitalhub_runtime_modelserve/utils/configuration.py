from __future__ import annotations

from digitalhub_runtime_modelserve.utils.frameworks.registry import config_function_registry


def get_function_args(action: str, root: str, model_path: str) -> None:
    """
    Get function arguments.

    Parameters
    ----------
    action : str
        The action.
    root : str
        Root path.
    model_path : str
        The model path.

    Returns
    -------
    None
    """
    config_function_registry[action](root, model_path)
