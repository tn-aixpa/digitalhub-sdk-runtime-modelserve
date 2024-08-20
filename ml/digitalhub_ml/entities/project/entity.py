from __future__ import annotations

import typing

from digitalhub_data.entities.project.entity import CTX_ENTITIES, FUNC_MAP, ProjectData
from digitalhub_ml.entities.entity_types import EntityTypes
from digitalhub_ml.entities.model.crud import (
    create_model_from_dict,
    delete_model,
    get_model,
    list_models,
    log_model,
    new_model,
)

if typing.TYPE_CHECKING:
    from digitalhub_ml.entities.model.entity import Model

MODELS = EntityTypes.MODEL.value
CTX_ENTITIES.append(MODELS)
FUNC_MAP[MODELS] = create_model_from_dict


class ProjectMl(ProjectData):
    """
    ProjectMl class.
    """

    ##############################
    #  Models
    ##############################

    def new_model(
        self,
        name: str,
        kind: str,
        uuid: str | None = None,
        description: str | None = None,
        labels: list[str] | None = None,
        embedded: bool = True,
        path: str | None = None,
        **kwargs,
    ) -> Model:
        """
        Create a new Model instance with the specified parameters.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        uuid : str
            ID of the object (UUID4).
        description : str
            Description of the object (human readable).
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object must be embedded in project.
        path : str
            Object path on local file system or remote storage.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Model
            An instance of the created model.
        """
        obj = new_model(
            project=self.name,
            name=name,
            kind=kind,
            uuid=uuid,
            description=description,
            labels=labels,
            embedded=embedded,
            path=path,
            **kwargs,
        )
        self.refresh()
        return obj

    def get_model(
        self,
        identifier: str,
        entity_id: str | None = None,
        **kwargs,
    ) -> Model:
        """
        Get object from backend.

        Parameters
        ----------
        identifier : str
            Entity key or name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Model
            Instance of Model class.
        """
        obj = get_model(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            **kwargs,
        )
        self.refresh()
        return obj

    def delete_model(
        self,
        identifier: str,
        entity_id: str | None = None,
        delete_all_versions: bool = False,
        **kwargs,
    ) -> None:
        """
        Delete a Model from project.

        Parameters
        ----------
        identifier : str
            Entity key or name.
        entity_id : str
            Entity ID.
        delete_all_versions : bool
            Delete all versions of the named entity.
            Use entity name instead of entity key as identifier.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        delete_model(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            delete_all_versions=delete_all_versions,
            **kwargs,
        )
        self.refresh()

    def list_models(self, **kwargs) -> list[dict]:
        """
        List models associated with the project.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[dict]
            List of objects related to project.
        """
        return list_models(self.name, **kwargs)

    def log_model(
        self,
        name: str,
        kind: str,
        source: str,
        path: str | None = None,
        **kwargs,
    ) -> Model:
        """
        Create and upload an model.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        source : str
            Model location on local machine.
        path : str
            Destination path of the model. If not provided, it's generated.
        **kwargs : dict
            New model parameters.

        Returns
        -------
        Model
            Instance of Model class.
        """
        obj = log_model(
            project=self.name,
            name=name,
            kind=kind,
            source=source,
            path=path,
            **kwargs,
        )
        self.refresh()
        return obj
