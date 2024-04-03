from __future__ import annotations

import os
import time
from typing import Callable

import kfp
from digitalhub_core_kfp.dsl import set_current_project, unset_current_project
from digitalhub_core_kfp.utils.outputs import build_status
from kfp_server_api.models import ApiRun

import digitalhub as dhcore


def run_kfp_pipeline(run: dict) -> any:
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

    def _kfp_execution(pipeline: Callable, function_args) -> dict:
        client = kfp.Client(host=os.environ.get("KFP_ENDPOINT"))
        # workaround to pass the project implicitly
        set_current_project(run.get("project"))
        result = client.create_run_from_pipeline_func(pipeline, arguments=function_args)
        unset_current_project()

        status = None
        response = None
        run_status = None
        while status is None or status.lower() not in ["succeeded", "failed", "skipped", "error"]:
            time.sleep(5)
            try:
                response = client.get_run(run_id=result.run_id)
                status = response.run.status
                run_status = build_status(response, client)
                # update status
                dhcore_run = dhcore.get_run(run.get("project"), run.get("id"))
                dhcore_run._set_status(run_status)
                dhcore_run.save(update=True)
            except Exception:
                pass
        return run_status

    return _kfp_execution
