from __future__ import annotations

from digitalhub_ml.entities.runs.spec import RunParamsMl, RunSpecMl


class RunSpecMlrun(RunSpecMl):
    """Run Mlrun specification."""

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


class RunParamsMlrun(RunParamsMl):
    """Run Mlrun parameters."""

    # Function parameters
    source: dict = None
    image: str = None
    tag: str = None
    handler: str = None
    command: str = None
    requirements: list = None

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

    # Task build
    target_image: str = None
    commands: list[str] = None
    force_build: bool = False
