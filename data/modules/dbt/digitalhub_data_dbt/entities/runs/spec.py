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
        local_execution: bool = False,
        function_spec: dict | None = None,
        transform_spec: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(task, inputs, outputs, parameters, local_execution, **kwargs)
        self.function_spec = function_spec
        self.transform_spec = transform_spec


class RunParamsDbt(RunParamsData):
    """Run Dbt parameters."""

    function_spec: dict = None
    """The function spec."""

    transform_spec: dict = None
    """The transform task spec."""
