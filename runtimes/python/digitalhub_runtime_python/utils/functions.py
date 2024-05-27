from __future__ import annotations

from typing import Callable


def run_python(func: Callable, *args, **kwargs) -> dict:
    """
    Execute function.

    Parameters
    ----------
    func : Callable
        Function.
    args : tuple
        Function arguments.
    kwargs : dict
        Function keyword arguments.

    Returns
    -------
    dict
        Outputs from the function.
    """
    return func(*args, **kwargs)
