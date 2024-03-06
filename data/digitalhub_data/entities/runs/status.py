"""
RunStatusData module.
"""
from __future__ import annotations

import typing

from digitalhub_core.entities.artifacts.crud import get_artifact_from_key
from digitalhub_core.entities.runs.status import EntitiesOutputs, RunStatus
from digitalhub_data.entities.dataitems.crud import get_dataitem_from_key

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_data.entities.dataitems.entity._base import Dataitem


class RunStatusData(RunStatus):
    """
    A class representing a run status.
    """

    def get_outputs(self) -> dict:
        """
        Get results.

        Returns
        -------
        dict
            The results.
        """
        artifacts = self.outputs.get("artifacts", [])
        artifact_objs = [get_artifact_from_key(dti.get("id")) for dti in artifacts]
        dataitems = self.outputs.get("dataitems", [])
        dataitems_objs = [get_dataitem_from_key(dti.get("id")) for dti in dataitems]
        return EntitiesOutputsData(artifacts=artifact_objs, dataitems=dataitems_objs)


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
