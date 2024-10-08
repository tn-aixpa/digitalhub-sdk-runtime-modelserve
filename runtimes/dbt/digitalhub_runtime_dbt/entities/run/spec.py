from __future__ import annotations

from digitalhub_data.entities.run.spec import RunParamsData, RunSpecData


class RunSpecDbt(RunSpecData):
    """Run Dbt specification."""

    def __init__(
        self,
        task: str,
        local_execution: bool = False,
        function: str | None = None,
        node_selector: dict | None = None,
        volumes: list | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list | None = None,
        envs: list | None = None,
        secrets: list | None = None,
        profile: str | None = None,
        source: dict | None = None,
        inputs: dict | None = None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            task,
            local_execution,
            function,
            node_selector,
            volumes,
            resources,
            affinity,
            tolerations,
            envs,
            secrets,
            profile,
            **kwargs,
        )
        self.source = source
        self.inputs = inputs
        self.outputs = outputs
        self.parameters = parameters


class RunParamsDbt(RunParamsData):
    """Run Dbt parameters."""

    # Function parameters
    source: dict = None

    # Run parameters
    inputs: dict = None
    outputs: dict = None
    parameters: dict = None
