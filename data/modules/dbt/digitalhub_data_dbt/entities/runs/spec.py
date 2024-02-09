from __future__ import annotations

from digitalhub_core.entities.runs.spec import RunParams, RunSpec


class RunSpecDbt(RunSpec):
    """Run Dbt specification."""

    def __init__(
        self,
        task: str,
        task_id: str,
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

        Parameters
        ----------
        """
        super().__init__(task, task_id, inputs, outputs, parameters, local_execution, **kwargs)
        self.function_spec = function_spec
        self.transform_spec = transform_spec


class RunParamsDbt(RunParams):
    """Run Dbt parameters."""

    function_spec: dict = None
    """The function spec."""

    transform_spec: dict = None
    """The transform task spec."""


spec_registry = {
    "dbt+run": [RunSpecDbt, RunParamsDbt],
}
