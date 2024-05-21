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
        function_spec: dict | None = None,
        job_spec: dict | None = None,
        nuclio_spec: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(task, inputs, outputs, parameters, values, local_execution, **kwargs)
        self.function_spec = function_spec
        self.job_spec = job_spec
        self.nuclio_spec = nuclio_spec


class RunParamsPython(RunParamsMl):
    """Run Python parameters."""

    function_spec: dict = None
    job_spec: dict = None
    nuclio_spec: dict = None
