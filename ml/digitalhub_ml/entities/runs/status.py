from __future__ import annotations

import typing

from digitalhub_core.entities.artifacts.crud import get_artifact_from_key
from digitalhub_data.entities.dataitems.crud import get_dataitem_from_key
from digitalhub_data.entities.runs.status import EntitiesOutputsData, RunStatusData
from digitalhub_ml.entities.models.crud import get_model_from_key

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_data.entities.dataitems.entity._base import Dataitem
    from digitalhub_ml.entities.models.entity import Model


class RunStatusMl(RunStatusData):
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
        models = self.outputs.get("models", [])
        model_objs = [get_model_from_key(dti.get("id")) for dti in models]
        return EntitiesOutputsMl(artifacts=artifact_objs, dataitems=dataitems_objs, models=model_objs)


class EntitiesOutputsMl(EntitiesOutputsData):
    """
    A class representing a run results.
    """

    def __init__(
        self,
        artifacts: list[Artifact] | None = None,
        dataitems: list[Dataitem] | None = None,
        models: list[Model] | None = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        dataitems : list[Dataitem]
            The dataitems.
        """
        super().__init__(artifacts, dataitems)
        self.models = models

    def get_models(self) -> list[Model]:
        """
        Get models.

        Returns
        -------
        list[Model]
            List of models.
        """
        return self.models if self.models is not None else []

    def get_model_by_name(self, name: str) -> Model | None:
        """
        Get model by name.

        Parameters
        ----------
        name : str
            Entity name.

        Returns
        -------
        Model
            Model.
        """
        for model in self.get_models():
            if model.name == name:
                return model
        return None
