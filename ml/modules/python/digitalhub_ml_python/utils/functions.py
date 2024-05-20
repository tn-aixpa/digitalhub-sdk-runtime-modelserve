from __future__ import annotations

from typing import Callable


def run_python_job(func: Callable, *args, **kwargs) -> dict:
    """
    Run Python job.

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


def run_python_nuclio():
    raise NotImplementedError
