from __future__ import annotations

from digitalhub_core.entities.runs.spec import RunParams, RunSpec
from pydantic import BaseModel


class RunSpecNefertem(RunSpec):
    """Run Nefertem specification."""

    def __init__(
        self,
        task: str,
        task_id: str,
        inputs: dict | None = None,
        outputs: dict | None = None,
        parameters: dict | None = None,
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

        Parameters
        ----------
        """
        super().__init__(task, task_id, inputs, outputs, parameters, local_execution, **kwargs)
        self.function_spec = function_spec
        self.infer_spec = infer_spec
        self.profile_spec = profile_spec
        self.validate_spec = validate_spec
        self.metric_spec = metric_spec


class DataitemList(BaseModel):
    """Dataitem list model."""

    dataitems: list[str]
    """List of dataitem names."""


class RunParamsNefertem(RunParams):
    """Run Nefertem parameters."""

    inputs: DataitemList
    """List of input dataitem names. Override RunSpec.inputs."""

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


spec_registry = {
    "nefertem+run": [RunSpecNefertem, RunParamsNefertem],
}
