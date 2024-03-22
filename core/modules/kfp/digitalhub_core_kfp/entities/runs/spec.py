from __future__ import annotations

from digitalhub_data.entities.runs.spec import RunParamsData, RunSpecData


class RunSpecKFP(RunSpecData):
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
        pipeline_spec: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        """
        super().__init__(task, inputs, outputs, parameters, values, local_execution, **kwargs)
        self.function_spec = function_spec
        self.pipeline_spec = pipeline_spec


class RunParamsKFP(RunParamsData):
    """Run KFP parameters."""

    function_spec: dict = None
    """The function spec."""

    pipeline_spec: dict = None
    """The pipeline task spec."""
