from __future__ import annotations

import typing

from digitalhub_data.entities.runs.outputs import EntitiesOutputsData

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.artifacts.entity import Artifact
    from digitalhub_data.entities.dataitems.entity._base import Dataitem
    from digitalhub_ml.entities.models.entity import Model


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

    def list_model_names(self) -> list[str]:
        """
        List model names.

        Returns
        -------
        list[str]
            List of model names.
        """
        return [i.name for i in self.get_models()]

    def get_model_by_key(self, key: str) -> Model | None:
        """
        Get model by key.

        Parameters
        ----------
        key : str
            Entity key.

        Returns
        -------
        Model
            Model.
        """
        for model in self.get_models():
            if model.key == key:
                return model
        return None

    def list_model_keys(self) -> list[str]:
        """
        List model keys.

        Returns
        -------
        list[str]
            List of model keys.
        """
        return [i.key for i in self.get_models()]
