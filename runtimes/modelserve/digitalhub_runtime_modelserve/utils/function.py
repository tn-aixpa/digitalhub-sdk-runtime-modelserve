from __future__ import annotations

from typing import Callable

from digitalhub_runtime_modelserve.utils.frameworks.registry import serve_function_registry


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
    return serve_function_registry[action]
