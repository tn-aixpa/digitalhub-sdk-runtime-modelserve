"""
RunStatus class module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.status import Status
from digitalhub_core.entities.runs.getter import EntityGetter
from digitalhub_core.entities.runs.outputs import EntitiesOutputs


class RunStatus(Status):
    """
    Status class for run entities.
    """

    def __init__(
        self,
        state: str,
        message: str | None = None,
        outputs: list | None = None,
        values: list | None = None,
        results: dict | None = None,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(state, message)
        self.outputs = outputs
        self.values = values
        self.results = results

    def get_results(self) -> dict:
        """
        Get results.

        Returns
        -------
        dict
            The results.
        """
        return self.results if self.results is not None else {}

    def get_outputs(self, project_name: str) -> EntitiesOutputs:
        """
        Get results.

        Returns
        -------
        dict
            The results.
        """
        outputs = EntityGetter().collect_entity(self.outputs, project_name)
        return EntitiesOutputs(**outputs)
