from __future__ import annotations

import os
import tempfile
from typing import Callable

import kfp
from kfp.compiler import compiler

from digitalhub.utils.generic_utils import encode_source


def run_kfp_build(pipeline: Callable, *args, **kwargs) -> dict:
    """
    Build KFP pipeline.

    Parameters
    ----------
    pipeline : Callable
        KFP pipeline function.

    Returns
    -------
    dict
        Pipeline spec.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        pipeline_package_path = os.path.join(tmpdir, "pipeline.yaml")
        compiler.Compiler(kfp.dsl.PipelineExecutionMode.V1_LEGACY).compile(
            pipeline_func=pipeline,
            package_path=pipeline_package_path,
        )
        return {"source": encode_source(pipeline_package_path), "lang": "yaml"}
