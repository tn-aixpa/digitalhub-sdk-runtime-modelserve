from __future__ import annotations

import typing
from typing import Callable

import os

from kfp_server_api.models import ApiRun
import kfp

def kfp_execution(pipeline: Callable, **function_args) -> ApiRun:
    
    client = kfp.Client(host=os.environ.get("KFP_ENDPOINT"))
    result = client.create_run_from_pipeline_func(pipeline, arguments=function_args)
    # TODO distinguish between local and remote for completion
    response: ApiRun = result.wait_for_run_completion()
    return response



def run_kfp_pipeline(pipeline: Callable, pipeline_args) -> ApiRun:
    """
    Run KFP pipeline.

    Parameters
    ----------
    pipeline : BaseRuntime
        KFP pipeline function.
    pipeline_args : dict
        Pipeline arguments.

    Returns
    -------
    dict
        Execution results.
    """
    
    return kfp_execution(pipeline, **pipeline_args)