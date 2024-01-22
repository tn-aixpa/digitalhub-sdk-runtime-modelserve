from __future__ import annotations

import typing
from typing import Callable

import nefertem

if typing.TYPE_CHECKING:
    from nefertem.client.client import Client


def create_client(output_path: str, store: dict) -> Client:
    """
    Create Nefertem client.

    Parameters
    ----------
    output_path : str
        Output path where to store Nefertem results.
    store : dict
        Store configuration.

    Returns
    -------
    Client
        Nefertem client.
    """
    client = nefertem.create_client(output_path=output_path)
    try:
        client.add_store(store)
    except nefertem.utils.exceptions.StoreError:
        pass
    return client


####################
# Tasks
####################


def select_function(action: str) -> Callable:
    """
    Select function according to action.

    Parameters
    ----------
    action : str
        Action to execute.

    Returns
    -------
    Callable
        Function to execute.
    """
    if action == "validate":
        return validate
    if action == "profile":
        return profile
    if action == "infer":
        return infer
    if action == "metric":
        return metric
    raise NotImplementedError


def infer(**kwargs) -> dict:
    """
    Execute infer task.

    Parameters
    ----------
    **kwargs : dict
        Nefertem client, resources, run_config, run_id

    Returns
    -------
    dict
        Nefertem run info.
    """
    client = kwargs.get("client")
    resources = kwargs.get("resources")
    run_config = kwargs.get("run_config")
    run_id = kwargs.get("run_id")

    with client.create_run(resources, run_config, run_id=run_id) as nt_run:
        nt_run.infer()
        nt_run.log_schema()
        nt_run.persist_schema()
    return nt_run.run_info.to_dict()


def profile(**kwargs) -> dict:
    """
    Execute profile task.

    Parameters
    ----------
    **kwargs : dict
        Nefertem client, resources, run_config, run_id

    Returns
    -------
    dict
        Nefertem run info.
    """
    client = kwargs.get("client")
    resources = kwargs.get("resources")
    run_config = kwargs.get("run_config")
    run_id = kwargs.get("run_id")

    with client.create_run(resources, run_config, run_id=run_id) as nt_run:
        nt_run.profile()
        nt_run.log_profile()
        nt_run.persist_profile()
    return nt_run.run_info.to_dict()


def validate(**kwargs) -> dict:
    """
    Execute validate task.

    Parameters
    ----------
    **kwargs : dict
        Nefertem client, resources, run_config, run_id, constraints and error_report

    Returns
    -------
    dict
        Nefertem run info.
    """
    client = kwargs.get("client")
    resources = kwargs.get("resources")
    run_config = kwargs.get("run_config")
    run_id = kwargs.get("run_id")
    constraints = kwargs.get("constraints")
    error_report = kwargs.get("error_report")

    with client.create_run(resources, run_config, run_id=run_id) as nt_run:
        nt_run.validate(constraints=constraints, error_report=error_report)
        nt_run.log_report()
        nt_run.persist_report()
    return nt_run.run_info.to_dict()


def metric(**kwargs) -> dict:
    """
    Execute metric task.

    Parameters
    ----------
    **kwargs : dict
        Nefertem client, resources, run_config, run_id and metrics

    Returns
    -------
    dict
        Nefertem run info.
    """
    client = kwargs.get("client")
    resources = kwargs.get("resources")
    run_config = kwargs.get("run_config")
    run_id = kwargs.get("run_id")
    metrics = kwargs.get("metrics")

    with client.create_run(resources, run_config, run_id=run_id) as nt_run:
        nt_run.metric(metrics=metrics)
        nt_run.log_metric()
        nt_run.persist_metric()
    return nt_run.run_info.to_dict()


####################
# Configuration
####################


def create_nt_resources(inputs: list[dict], store: dict) -> list[dict]:
    """
    Create nefertem resources.

    Parameters
    ----------
    inputs : list
        The list of inputs dataitems.
    store : dict
        The store configuration.

    Returns
    -------
    list[dict]
        The list of nefertem resources.
    """
    resources = []
    for i in inputs:
        res = {}
        res["name"] = i["name"]
        res["path"] = i["path"]
        res["store"] = store["name"]
        resources.append(res)
    return resources


def create_nt_run_config(action: str, spec: dict) -> dict:
    """
    Build nefertem run configuration.

    Parameters
    ----------
    spec : dict
        Run specification.

    Returns
    -------
    dict
        The nefertem run configuration.
    """
    if action == "infer":
        operation = "inference"
    elif action == "profile":
        operation = "profiling"
    elif action == "validate":
        operation = "validation"
    elif action == "metric":
        operation = "metric"
    return {
        "operation": operation,
        "exec_config": [
            {
                "framework": spec.get("framework"),
                "exec_args": spec.get("exec_args", {}),
            }
        ],
        "parallel": spec.get("parallel", False),
        "num_worker": spec.get("num_worker", 1),
    }
