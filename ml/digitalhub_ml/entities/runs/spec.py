"""
Run base specification module.
"""
from __future__ import annotations

import typing

from digitalhub_data.entities.runs.spec import RunParamsData, RunSpecData
from digitalhub_ml.entities.runs.getter import EntityGetterMl
from digitalhub_ml.entities.runs.models import EntityInputsOutputsMl

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity import Entity


class RunSpecMl(RunSpecData):
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
        return EntityGetterMl().collect_entity(self.inputs, project_name)


class RunParamsMl(RunParamsData):
    """
    Run parameters.
    """

    inputs: EntityInputsOutputsMl = None
    """Run inputs."""

    outputs: EntityInputsOutputsMl = None
    """Run outputs."""
