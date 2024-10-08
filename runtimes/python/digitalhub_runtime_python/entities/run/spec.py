from __future__ import annotations

from digitalhub_ml.entities.run.spec import RunParamsMl, RunSpecMl


class RunSpecPython(RunSpecMl):
    """Run Python specification."""

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
        image: str | None = None,
        base_image: str | None = None,
        python_version: str | None = None,
        requirements: list | None = None,
        instructions: dict | None = None,
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
        self.image = image
        self.base_image = base_image
        self.python_version = python_version
        self.requirements = requirements
        self.instructions = instructions
        self.inputs = inputs
        self.outputs = outputs
        self.parameters = parameters


class RunParamsPython(RunParamsMl):
    """Run Python parameters."""

    # Function parameters
    source: dict = None
    image: str = None
    base_image: str = None
    python_version: str = None
    requirements: list = None

    # Task job
    backoff_limit: int = None

    # Task serve
    service_type: str = None
    replicas: int = None

    # Task build
    instructions: list[str] = None

    # Run parameters
    inputs: dict = None
    outputs: dict = None
    parameters: dict = None
