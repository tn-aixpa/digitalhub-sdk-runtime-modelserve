from __future__ import annotations

import typing

from mlrun import run_function

if typing.TYPE_CHECKING:
    from mlrun.runtimes import BaseRuntime
    from mlrun.runtimes.base import RunObject


def run_job(function: BaseRuntime, function_args: dict) -> RunObject:
    """
    Run Mlrun job.

    Parameters
    ----------
    function : BaseRuntime
        Mlrun function.
    function_args : dict
        Function arguments.

    Returns
    -------
    dict
        Execution results.
    """
    function_args["local"] = True
    return run_function(function, **function_args)
