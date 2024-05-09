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
        function_spec: dict | None = None,
        job_spec: dict | None = None,
        build_spec: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(task, inputs, outputs, parameters, values, local_execution, **kwargs)
        self.function_spec = function_spec
        self.job_spec = job_spec
        self.build_spec = build_spec


class RunParamsMlrun(RunParamsMl):
    """Run Mlrun parameters."""

    function_spec: dict = None
    """The function spec."""

    job_spec: dict = None
    """The job task spec."""

    build_spec: dict = None
    """The build task spec."""
