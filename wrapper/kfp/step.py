"""
Wrapper to execute an arbitrary function.
"""
import os
import argparse
from pathlib import Path
import json
import time

from digitalhub_core.utils.logger import LOGGER

import digitalhub as dhcore

def _is_finished(state: str):
    return state == "COMPLETED" or state == "ERROR" or state == "STOPPED"

def _is_complete(state: str):
    return state == "COMPLETED"

def execute_step(project, function, action, jsonprops=None, inputs={}, outputs={}, parameters={}, values=[], args=None):
    """
    Execute a step.
    """
    
    LOGGER.info("Loading project " + project)
    project = dhcore.get_project(project)
    
    LOGGER.info("Executing function " + function +' task ' + action)
    function = project.get_function(function)

    if jsonprops is not None:
        props = json.loads(jsonprops)
    else:
        props = {}

    if args is None:
        args = {}

    run = function.run(action,
                       node_selector=props.get("node_selector") if "node_selector" in props else None,
                       volumes=props.get("volumes") if "volumes" in props else None,
                       resources=props.get("resources") if "resources" in props else None,
                       env=props.get("env") if "env" in props else None,
                       secrets=props.get("secrets") if "secrets" in props else None,
                       inputs=inputs,
                       outputs=outputs,
                       parameters=parameters,
                       values=values,
                       **args
                       )

    # Wait for the run to complete
    while not _is_finished(run.status.state):
        time.sleep(5)
        run = run.refresh()
        LOGGER.info("Step state: " + run.status.state)

    # If the run is complete process outputs
    if _is_complete(run.status.state):
        LOGGER.info("Step completed: " + run.status.state)
        # process entities
        for o in run.outputs():
            for prop, val in o.items():
                if prop in outputs:
                    # write to file val 
                    target_output = f"/tmp/entity_{outputs[prop]}"
                    target_output = Path(target_output)
                    target_output.parent.mkdir(parents=True, exist_ok=True)
                    with open(target_output, "w") as f:
                        f.write(val)
    
        # process values
        for o in run.values():
            for prop, val in o.items():
                if prop in values:
                    # write to file val 
                    target_output = f"/tmp/value_{outputs[prop]}"
                    target_output = Path(target_output)
                    target_output.parent.mkdir(parents=True, exist_ok=True)
                    with open(target_output, "w") as f:
                        f.write(val)
        LOGGER.info("Done.")
    else:
        LOGGER.info("Step failed: " + run.status.state)
        exit(1)

def parser():
    
    parser = argparse.ArgumentParser(description='Step executor')

    parser.add_argument('--project', type=str, help='Project reference', required=True)
    parser.add_argument('--function', type=str, help='Function name', required=True)
    parser.add_argument('--action', type=str, help='Action type', required=True)
    parser.add_argument('--jsonprops', type=str, help='Function execution properties in JSON format', required=False)
    parser.add_argument('--parameters', type=str, help='Function parameters', required=False)
    parser.add_argument('-a', type=str, action='append', help='Function args', required=False)
    parser.add_argument('-ie', action='append', type=str, help='Input entity property', required=False)
    parser.add_argument('-iv', action='append', type=str, help='Input value property', required=False)
    parser.add_argument('-oe', action='append', type=str, help='Output entity property', required=False)
    parser.add_argument('-ov', action='append', type=str, help='Output value property', required=False)
    return parser

def main(args):
    """
    Main function. Get run from backend and execute function.
    """

    inputs = []
    if args.ie is not None:
        for ie in args.ie:
            ie_param = ie[0:ie.find("=")]
            ie_value = ie[ie.find("=")+1:]
            inputs.append({ie_param : ie_value})

    parameters = {}
    if args.iv is not None:
        for iv in args.iv:
            iv_param = iv[0:iv.find("=")]
            iv_value = iv[iv.find("=")+1:]
            parameters[iv_param] = iv_value

    outputs = []
    if args.oe is not None:
        for oe in args.oe:
            oe_param = oe[0:oe.find("=")]
            oe_value = oe[oe.find("=")+1:]
            outputs.append({oe_param : oe_value})

    values = []
    if args.ov is not None:
        for ov in args.ov:
            values.append(ov)

    step_args = {}
    if args.a is not None:
        for a in args.a:
            p = a.split("=")
            step_args[p[0]] = p[1]
    
    execute_step(args.project, args.function, args.action, args.jsonprops, inputs, outputs, parameters, values, step_args)


if __name__ == "__main__":
    # Defining and parsing the command-line arguments
    args = parser().parse_args()

    main(args)
