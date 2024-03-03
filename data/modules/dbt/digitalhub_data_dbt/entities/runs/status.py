from __future__ import annotations

from digitalhub_core.entities.runs.status import RunStatus
from digitalhub_data.entities.dataitems.crud import get_dataitem_from_key
from digitalhub_data.entities.runs.results import RunResultsData


class RunStatusDbt(RunStatus):
    """
    Run Dbt status.
    """

    def __init__(
        self,
        state: str | None = None,
        message: str | None = None,
        results: dict | None = None,
        outputs: dict | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        results : dict
            Runtime results.
        outputs : dict
            Runtime entities outputs.
        **kwargs
            Keyword arguments.


        See Also
        --------
        Status.__init__
        """
        super().__init__(state, message)
        self.results = results
        self.outputs = outputs

    def get_results(self) -> dict:
        """
        Get results.

        Returns
        -------
        dict
            The results.
        """
        dataitems = self.outputs.get("dataitems", [])
        dataitem_objs = [get_dataitem_from_key(dti.get("id")) for dti in dataitems]
        return RunResultsData(dataitems=dataitem_objs)
