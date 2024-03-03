from __future__ import annotations

from digitalhub_core.entities.artifacts.crud import get_artifact_from_key
from digitalhub_core.entities.runs.status import RunStatus
from digitalhub_data.entities.dataitems.crud import get_dataitem_from_key
from digitalhub_ml.entities.models.crud import get_model_from_key
from digitalhub_ml.entities.runs.results import RunResultsMl


class RunStatusMlrun(RunStatus):
    """
    Run Mlrun status.
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
        artifact_objs = [get_artifact_from_key(dti.get("id")) for dti in artifacts]
        dataitems = self.outputs.get("dataitems", [])
        dataitems_objs = [get_dataitem_from_key(dti.get("id")) for dti in dataitems]
        models = self.outputs.get("models", [])
        model_objs = [get_model_from_key(dti.get("id")) for dti in models]
        return RunResultsMl(artifacts=artifact_objs, dataitems=dataitems_objs, models=model_objs)
