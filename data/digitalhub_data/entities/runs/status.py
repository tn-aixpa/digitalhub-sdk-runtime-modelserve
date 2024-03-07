"""
RunStatusData module.
"""
from __future__ import annotations

from digitalhub_core.entities.runs.status import RunStatus
from digitalhub_data.entities.runs.getter import EntityGetterData
from digitalhub_data.entities.runs.outputs import EntitiesOutputsData


class RunStatusData(RunStatus):
    """
    A class representing a run status.
    """

    def get_outputs(self, project_name: str) -> EntitiesOutputsData:
        """
        Get results.

        Parameters
        ----------
        project_name : str
            Name of the project.

        Returns
        -------
        dict
            The results.
        """
        outputs = EntityGetterData().collect_entity(self.outputs, project_name)
        return EntitiesOutputsData(**outputs)
