"""
Run base specification module.
"""
from __future__ import annotations

import typing

from digitalhub_core.entities._base.spec import Spec, SpecParams
from digitalhub_core.entities.runs.getter import EntityGetter
from digitalhub_core.entities.runs.models import EntityInputsOutputs

if typing.TYPE_CHECKING:
    from digitalhub_core.entities._base.entity import Entity


class RunSpec(Spec):
    """Run specification."""

    def __init__(
        self,
        task: str,
        inputs: dict | None = None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        local_execution: bool = False,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        task : str
            The task associated with the run.
        inputs : dict
            The inputs of the run.
        outputs : dict
            The outputs of the run.
        parameters : dict
            The parameters for the run.
        local_execution : bool
            Flag to indicate if the run will be executed locally
        **kwargs
            Keywords arguments.
        """
        self.task = task
        self.inputs = inputs if inputs is not None else {}
        self.outputs = outputs if outputs is not None else {}
        self.parameters = parameters if parameters is not None else {}
        self.local_execution = local_execution

    def get_inputs(self, project_name: str) -> dict[str, list[Entity]]:
        """
        Get inputs.

        Parameters
        ----------
        project_name : str
            Name of the project.

        Returns
        -------
        dict[str, list[Entity]]
            The inputs.
        """
        return EntityGetter().collect_entity(self.inputs, project_name)


class RunParams(SpecParams):
    """
    Run parameters.
    """

    task: str = None
    """The task string associated with the run."""

    inputs: EntityInputsOutputs = None
    """Run inputs."""

    outputs: EntityInputsOutputs = None
    """Run outputs."""

    parameters: dict = None
    """Parameters to be used in the run."""

    local_execution: bool = False
    """Flag to indicate if the run will be executed locally."""
