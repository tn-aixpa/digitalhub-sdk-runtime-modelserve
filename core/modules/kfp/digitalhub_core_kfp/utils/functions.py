from __future__ import annotations

import os
from typing import Callable

import kfp
from kfp_server_api.models import ApiRun

from ..dsl import set_current_project, unset_current_project


def kfp_execution(pipeline: Callable, **function_args) -> ApiRun:
    client = kfp.Client(host=os.environ.get("KFP_ENDPOINT"))
    # workaround to pass the project implicitly
    set_current_project(function_args["_project_name"])
    function_args.pop("_project_name", None)
    result = client.create_run_from_pipeline_func(pipeline, arguments=function_args)
    unset_current_project()

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
