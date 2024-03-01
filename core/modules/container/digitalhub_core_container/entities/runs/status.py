from __future__ import annotations

from digitalhub_core.entities.artifacts.crud import get_artifact_from_key
from digitalhub_core.entities.runs.results import RunResults
from digitalhub_core.entities.runs.status import RunStatus


class RunStatusContainer(RunStatus):
    """
    Run Container status.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

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
        return RunResults(artifacts=artifact_objs)
