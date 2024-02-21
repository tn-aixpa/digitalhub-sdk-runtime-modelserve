from __future__ import annotations

import typing
from typing import Callable

import os

from kfp_server_api.models import ApiRun
import kfp

def kfp_execution(pipeline: Callable, function_args: dict) -> ApiRun:
    
    client = kfp.Client(host=os.environ.get("KFP_ENDPOINT"))
    result = client.create_run_from_pipeline_func(pipeline, arguments=function_args)
    response: ApiRun = result.wait_for_run_completion()
    return response



def run_kfp_pipeline(pipeline: Callable, function_args: dict) -> ApiRun:
    """
    Run KFP pipeline.

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
    
    return kfp_execution(function, **function_args)