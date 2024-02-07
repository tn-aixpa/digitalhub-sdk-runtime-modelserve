from __future__ import annotations

from digitalhub_core.entities.runs.spec import RunParams, RunSpec


class RunSpecMlrun(RunSpec):
    """Run Mlrun specification."""

    def __init__(
        self,
        task: str,
        task_id: str,
        inputs: dict | None = None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        local_execution: bool = False,
        function_spec: dict | None = None,
        task_spec: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        """
        super().__init__(task, task_id, inputs, outputs, parameters, local_execution, **kwargs)
        self.function_spec = function_spec
        self.task_spec = task_spec


class RunParamsMlrun(RunParams):
    """Run Mlrun parameters."""

    function_spec: dict = None
    """The function spec."""

    task_spec: dict = None
    """The task spec."""


spec_registry = {
    "mlrun+run": [RunSpecMlrun, RunParamsMlrun],
}
