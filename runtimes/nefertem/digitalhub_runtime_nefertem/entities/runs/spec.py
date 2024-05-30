from __future__ import annotations

from digitalhub_data.entities.runs.spec import RunParamsData, RunSpecData


class RunSpecNefertem(RunSpecData):
    """Run Nefertem specification."""

    def __init__(
        self,
        task: str,
        inputs: dict | None = None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        values: list | None = None,
        local_execution: bool = False,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(task, inputs, outputs, parameters, values, local_execution)

        self._any_setter(**kwargs)


class RunParamsNefertem(RunParamsData):
    """Run Nefertem parameters."""

    # Function parameters
    constraints: list[dict] = None
    error_report: str = None
    metrics: list[dict] = None

    # Task parameters
    function: str = None
    node_selector: list[dict] = None
    volumes: list[dict] = None
    resources: list[dict] = None
    affinity: dict = None
    tolerations: list[dict] = None
    env: list[dict] = None
    secrets: list[str] = None
    backoff_limit: int = None
    schedule: str = None
    replicas: int = None
    framework: str = None
    exec_args: dict = None
    parallel: bool = None
    num_worker: int = None
