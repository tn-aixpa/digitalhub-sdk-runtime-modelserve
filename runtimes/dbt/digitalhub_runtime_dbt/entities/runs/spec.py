from __future__ import annotations

from digitalhub_data.entities.runs.spec import RunParamsData, RunSpecData


class RunSpecDbt(RunSpecData):
    """Run Dbt specification."""

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


class RunParamsDbt(RunParamsData):
    """Run Dbt parameters."""

    # Function parameters
    source: dict = None

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
