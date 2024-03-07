"""
RunStatusData module.
"""
from __future__ import annotations

import typing

from digitalhub_core.entities.runs.status import EntitiesOutputs, RunStatus
from digitalhub_data.entities.runs.getter import EntityGetterData

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_data.entities.dataitems.entity._base import Dataitem


class RunStatusData(RunStatus):
    """
    A class representing a run status.
    """

    def get_outputs(self, project_name: str) -> dict:
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
        return EntitiesOutputsData(**outputs).to_dict()


class EntitiesOutputsData(EntitiesOutputs):
    """
    A class representing a run results.
    """

    def __init__(
        self,
        artifacts: list[Artifact] | None = None,
        dataitems: list[Dataitem] | None = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        dataitems : list[Dataitem]
            The dataitems.
        """
        super().__init__(artifacts)
        self.dataitems = dataitems

    def get_dataitems(self) -> list[Dataitem]:
        """
        Get dataitems.

        Returns
        -------
        list[Dataitem]
            List of dataitems.
        """
        return self.dataitems if self.dataitems is not None else []

    def get_dataitem_by_name(self, name: str) -> Dataitem | None:
        """
        Get dataitem by name.

        Parameters
        ----------
        name : str
            Entity name.

        Returns
        -------
        Dataitem
            Dataitem.
        """
        for dataitem in self.get_dataitems():
            if dataitem.name == name:
                return dataitem
        return None
