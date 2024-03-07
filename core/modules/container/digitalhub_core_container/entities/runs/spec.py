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
        local_execution: bool = False,
        function_spec: dict | None = None,
        job_spec: dict | None = None,
        deploy_spec: dict | None = None,
        serve_spec: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(task, inputs, outputs, parameters, local_execution, **kwargs)
        self.function_spec = function_spec
        self.job_spec = job_spec
        self.deploy_spec = deploy_spec
        self.serve_spec = serve_spec


class RunParamsContainer(RunParams):
    """Run Container parameters."""

    function_spec: dict | None = None
    job_spec: dict | None = None
    deploy_spec: dict | None = None
    serve_spec: dict | None = None
