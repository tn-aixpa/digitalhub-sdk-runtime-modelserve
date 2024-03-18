from __future__ import annotations

from kubernetes import client as k8s_client
from kfp import dsl
import json
import os


def step(
        project: str,
        name: str,
        function: str,
        action: str,
        node_selector: list[dict] | None = None,
        volumes: list[dict] | None = None,
        resources: list[dict] | None = None,
        env: list[dict] | None = None,
        secrets: list[str] | None = None,
        inputs: list[dict] | None = None,
        outputs: list[dict] | None = None,
        parameters: list[dict] | None = None,
        values: list[str] | None = None,
        **kwargs) -> dsl.ContainerOp:
    
    WORKFLOW_IMAGE = os.environ.get("DIGITALHUB_CORE_WORKFLOW_IMAGE")
    KFPMETA_DIR = os.environ.get("KFPMETA_OUT_DIR", "/tmp")
    DIGITALHUB_CORE_ENDPOINT = os.environ.get('DIGITALHUB_CORE_ENDPOINT', 'http://localhost:8080/')

    props = {
        "node_selector": node_selector,
        "volumes": volumes,
        "resources": resources,
        "env": env,
        "secrets": secrets
    }
    
    parameters = {} if parameters is None else parameters
    inputs = [] if inputs is None else inputs
    outputs = [] if outputs is None else outputs
    values = [] if values is None else values

    args = {}
    if kwargs is not None:
        args.update(kwargs)
    
    file_outputs = {
        "mlpipeline-ui-metadata": KFPMETA_DIR + "/mlpipeline-ui-metadata.json",
        "mlpipeline-metrics": KFPMETA_DIR + "/mlpipeline-metrics.json",
    }
    
    cmd = [
        "python", "step.py",
        "--project", project,
        "--function", function,
        "--action", action,
        "--jsonprops", json.dumps(props),
    ]
    # simple input parameters and kwargs
    for param, val in args.items():
        cmd += ["-a", f"{param}={val}"]

    # complex input parameters
    for dict in inputs:
        for param, val in dict.items():
            cmd += ["-ie", f"{param}={val}"]

    # simple input parameters
    for param, val in parameters.items():
        cmd += ["-iv", f"{param}={val}"]

    # complex output parameters
    for dict in outputs:
        for param, val in dict.items():
            cmd += ["-oe", f"{param}={val}"]
            if isinstance(val, dsl.PipelineParam):
                oname = val.full_name
            else:
                oname = str(val)
            file_outputs[oname.replace(".", "_")] = (
                f"/tmp/entity_{oname}"  # not using path.join to avoid windows "\"
            )

    for param in values:
        cmd += ["-ov", f"{param}"]
        file_outputs[param.replace(".", "_")] = (
            f"/tmp/value_{val}"  # not using path.join to avoid windows "\"
        )
    
    cop = dsl.ContainerOp(
        name=name,
        image=WORKFLOW_IMAGE,
        command=cmd,
        file_outputs=file_outputs,
    )
    cop.container.add_env_variable(
            k8s_client.V1EnvVar(name="DIGITALHUB_CORE_ENDPOINT", value=DIGITALHUB_CORE_ENDPOINT)
        )

    return cop
    