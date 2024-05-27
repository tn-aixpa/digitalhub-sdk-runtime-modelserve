from __future__ import annotations

from digitalhub_ml.entities.runs.spec import RunParamsMl, RunSpecMl


class RunSpecPython(RunSpecMl):
    """Run Python specification."""

    def __init__(
        self,
        task: str,
        inputs: dict | None = None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        values: list | None = None,
        local_execution: bool = False,
        function: str | None = None,
        source: dict | None = None,
        image: str | None = None,
        base_image: str | None = None,
        requirements: list | None = None,
        node_selector: list[dict] | None = None,
        volumes: list[dict] | None = None,
        resources: list[dict] | None = None,
        affinity: dict | None = None,
        tolerations: list[dict] | None = None,
        env: list[dict] | None = None,
        secrets: list[str] | None = None,
        backoff_limit: int | None = None,
        schedule: str | None = None,
        replicas: int | None = None,
        context_refs: list[dict] | None = None,
        context_sources: list[dict] | None = None,
        instructions: list[str] | None = None,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(task, inputs, outputs, parameters, values, local_execution)

        # Function parameters
        self.source = source
        self.image = image
        self.base_image = base_image
        self.requirements = requirements

        # Task parameters
        self.function = function
        self.node_selector = node_selector
        self.volumes = volumes
        self.resources = resources
        self.affinity = affinity
        self.tolerations = tolerations
        self.env = env
        self.secrets = secrets
        self.backoff_limit = backoff_limit
        self.schedule = schedule
        self.replicas = replicas

        # Task build
        self.context_refs = context_refs
        self.context_sources = context_sources
        self.instructions = instructions


class RunParamsPython(RunParamsMl):
    """Run Python parameters."""

    # Function parameters
    source: dict = None
    image: str = None
    base_image: str = None
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
    context_refs: list[dict] = None
    context_sources: list[dict] = None
    instructions: list[str] = None
