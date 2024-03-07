from __future__ import annotations

import typing

from digitalhub_core.entities.runs.outputs import EntitiesOutputs

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_data.entities.dataitems.entity._base import Dataitem


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

    def list_dataitem_names(self) -> list[str]:
        """
        List dataitem names.

        Returns
        -------
        list[str]
            List of dataitem names.
        """
        return [i.name for i in self.get_dataitems()]

    def get_dataitem_by_key(self, key: str) -> Dataitem | None:
        """
        Get dataitem by key.

        Parameters
        ----------
        key : str
            Entity key.

        Returns
        -------
        Dataitem
            Dataitem.
        """
        for dataitem in self.get_dataitems():
            if dataitem.key == key:
                return dataitem
        return None

    def list_dataitem_keys(self) -> list[str]:
        """
        List dataitem keys.

        Returns
        -------
        list[str]
            List of dataitem keys.
        """
        return [i.key for i in self.get_dataitems()]
