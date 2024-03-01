from __future__ import annotations

from digitalhub_core.entities.artifacts.crud import get_artifact_from_key
from digitalhub_core.entities.runs.status import RunStatus
from digitalhub_data.entities.runs.results import RunResultsData


class RunStatusNefertem(RunStatus):
    """
    Run Nefertem status.
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
        artifacts = self.outputs.get("artifacts", [])
        artifact_objs = [get_artifact_from_key(art.get("id")) for art in artifacts]
        return RunResultsData(artifacts=artifact_objs)
