from __future__ import annotations

from digitalhub_core.entities.runs.spec import RunParams, RunSpec


class RunSpecContainer(RunSpec):
    """Run Container specification."""

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


class RunParamsContainer(RunParams):
    """Run Container parameters."""

    # Function parameters
    image: str = None
    base_image: str = None
    command: str = None
    args: list[str] = None

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

    # Task serve
    service_ports: list[dict] = None
    service_type: str = None

    # Task build
    context_refs: list[dict] = None
    context_sources: list[dict] = None
    instructions: list[str] = None
