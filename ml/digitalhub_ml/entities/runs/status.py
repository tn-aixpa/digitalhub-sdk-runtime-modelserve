from __future__ import annotations

from digitalhub_data.entities.runs.status import RunStatusData
from digitalhub_ml.entities.runs.getter import EntityGetterMl
from digitalhub_ml.entities.runs.outputs import EntitiesOutputsMl


class RunStatusMl(RunStatusData):
    def get_outputs(self, project_name: str) -> EntitiesOutputsMl:
        """
        Get results.

        Parameters
        ----------
        project_name : str
            Project name.

        Returns
        -------
        dict
            The results.
        """
        outputs = EntityGetterMl().collect_entity(self.outputs, project_name)
        return EntitiesOutputsMl(**outputs)
