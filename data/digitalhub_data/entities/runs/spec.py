"""
Run base specification module.
"""
from __future__ import annotations

from digitalhub_core.entities.runs.spec import RunParams, RunSpec
from digitalhub_data.entities.runs.models import EntityInputsOutputsData


class RunSpecData(RunSpec):
    """Run specification."""

    def get_inputs(self) -> dict:
        """
        Get inputs.

        Returns
        -------
        dict
            The inputs of the run.
        """
        return self.inputs


class RunParamsData(RunParams):
    """
    Run parameters.
    """

    inputs: EntityInputsOutputsData = None
    """Run inputs."""

    outputs: EntityInputsOutputsData = None
    """Run outputs."""
