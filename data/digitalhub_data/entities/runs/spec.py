"""
Run base specification module.
"""
from __future__ import annotations

import typing

from digitalhub_core.entities.runs.spec import RunParams, RunSpec
from digitalhub_data.entities.runs.getter import EntityGetterData
from digitalhub_data.entities.runs.models import EntityInputsOutputsData

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity import Entity


class RunSpecData(RunSpec):
    """Run specification."""

    def get_inputs(self, project_name: str) -> dict[str, list[Entity]]:
        """
        Get inputs.

        Parameters
        ----------
        project_name : str
            Name of the project.

        Returns
        -------
        dict
            The inputs of the run.
        """
        return EntityGetterData().collect_entity(self.inputs, project_name)


class RunParamsData(RunParams):
    """
    Run parameters.
    """

    inputs: EntityInputsOutputsData = None
    """Run inputs."""

    outputs: EntityInputsOutputsData = None
    """Run outputs."""
