from __future__ import annotations

from digitalhub_core.entities.runs.spec import RunParams, RunSpec
from pydantic import BaseModel


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
        job_spec: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        """
        super().__init__(task, task_id, inputs, outputs, parameters, local_execution, **kwargs)
        self.function_spec = function_spec
        self.job_spec = job_spec


class DataitemInputs(BaseModel):
    """Dataitem inputs model."""

    dataitems: dict[str, str]
    """Pairs of mlrun input dataitem variable and dhcore dataitem names."""


class RunParamsMlrun(RunParams):
    """Run Mlrun parameters."""

    inputs: DataitemInputs
    """List of pairs of input variable and dataitem names. Override RunSpec.inputs."""

    function_spec: dict = None
    """The function spec."""

    job_spec: dict = None
    """The job task spec."""


spec_registry = {
    "mlrun+run": [RunSpecMlrun, RunParamsMlrun],
}
