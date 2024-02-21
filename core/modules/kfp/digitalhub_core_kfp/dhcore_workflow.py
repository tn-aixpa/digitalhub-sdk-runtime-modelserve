from kfp import dsl
import json
import os

WORKFLOW_IMAGE = "dhcore/workflow-base"
KFPMETA_DIR = os.environ.get("KFPMETA_OUT_DIR", "/tmp")

def step(
        name: str,
        project: str,
        function: str,
        action: str,
        node_selector: list[dict] | None = None,
        volumes: list[dict] | None = None,
        resources: list[dict] | None = None,
        env: list[dict] | None = None,
        secrets: list[str] | None = None,
        inputs: dict | None = None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        **kwargs) -> dsl.ContainerOp:
    
    props = {
        "node_selector": node_selector,
        "volumes": volumes,
        "resources": resources,
        "env": env,
        "secrets": secrets,
        "parameters": parameters
    }
    
    if kwargs is not None:
        props.update(kwargs)
    
    cmd = [
        "python", "wrapper.py",
        "--project", project,
        "--function", function,
        "--action", action,
        "--json-props", json.dumps(props)
    ]
    
    cop = dsl.ContainerOp(
        name=name,
        image=WORKFLOW_IMAGE,
        command=cmd,
        file_outputs={
            "mlpipeline-ui-metadata": KFPMETA_DIR + "/mlpipeline-ui-metadata.json",
            "mlpipeline-metrics": KFPMETA_DIR + "/mlpipeline-metrics.json",
        },
    )

    return cop
    