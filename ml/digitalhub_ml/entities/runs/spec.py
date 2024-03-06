"""
Run base specification module.
"""
from __future__ import annotations

from digitalhub_data.entities.runs.spec import RunParamsData, RunSpecData
from digitalhub_ml.entities.runs.models import EntityInputsOutputsMl


class RunSpecMl(RunSpecData):
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


class RunParamsMl(RunParamsData):
    """
    Run parameters.
    """

    inputs: EntityInputsOutputsMl = None
    """Run inputs."""

    outputs: EntityInputsOutputsMl = None
    """Run outputs."""
