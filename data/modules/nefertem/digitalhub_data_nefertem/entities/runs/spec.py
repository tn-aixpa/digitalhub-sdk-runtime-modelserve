from __future__ import annotations

from digitalhub_data.entities.runs.spec import RunParamsData, RunSpecData


class RunSpecNefertem(RunSpecData):
    """Run Nefertem specification."""

    def __init__(
        self,
        task: str,
        inputs: list | None = None,
        outputs: list | None = None,
        parameters: dict | None = None,
        values: list | None = None,
        local_execution: bool = False,
        function_spec: dict | None = None,
        infer_spec: dict | None = None,
        profile_spec: dict | None = None,
        validate_spec: dict | None = None,
        metric_spec: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(task, inputs, outputs, parameters, values, local_execution, **kwargs)
        self.function_spec = function_spec
        self.infer_spec = infer_spec
        self.profile_spec = profile_spec
        self.validate_spec = validate_spec
        self.metric_spec = metric_spec


class RunParamsNefertem(RunParamsData):
    """Run Nefertem parameters."""

    function_spec: dict = None
    """The function spec."""

    infer_spec: dict = None
    """The infer task spec."""

    profile_spec: dict = None
    """The profile task spec."""

    validate_spec: dict = None
    """The validate task spec."""

    metric_spec: dict = None
    """The metric task spec."""
