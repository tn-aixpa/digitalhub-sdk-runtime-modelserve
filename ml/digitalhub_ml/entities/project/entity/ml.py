from __future__ import annotations

import typing

from digitalhub_data.entities.project.entity.data import CTX_ENTITIES, FUNC_MAP, ProjectData
from digitalhub_ml.entities.entity_types import EntityTypes
from digitalhub_ml.entities.model.crud import (
    delete_model,
    get_model,
    get_model_versions,
    import_model,
    list_models,
    log_model,
    model_from_dict,
    new_model,
    update_model,
)

if typing.TYPE_CHECKING:
    from digitalhub_ml.entities.model.entity._base import Model

MODELS = EntityTypes.MODEL.value
CTX_ENTITIES.append(MODELS)
FUNC_MAP[MODELS] = model_from_dict


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
        Create a new object.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        uuid : str
            ID of the object (UUID4, e.g. 40f25c4b-d26b-4221-b048-9527aff291e2).
        description : str
            Description of the object (human readable).
        labels : list[str]
            List of labels.
        embedded : bool
            Flag to determine if object spec must be embedded in project spec.
        path : str
            Object path on local file system or remote storage. It is also the destination path of upload() method.
        **kwargs : dict
            Spec keyword arguments.

        Returns
        -------
        Model
            Object instance.

        Examples
        --------
        >>> obj = project.new_model(name="my-model",
        >>>                            kind="model",
        >>>                            path="s3://my-bucket/my-key")
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

    def log_model(
        self,
        name: str,
        kind: str,
        source: str,
        path: str | None = None,
        **kwargs,
    ) -> Model:
        """
        Create and upload an object.

        Parameters
        ----------
        name : str
            Object name.
        kind : str
            Kind the object.
        source : str
            Model location on local path.
        path : str
            Destination path of the model. If not provided, it's generated.
        **kwargs : dict
            New model spec parameters.

        Returns
        -------
        Model
            Object instance.

        Examples
        --------
        >>> obj = project.log_model(name="my-model",
        >>>                            kind="model",
        >>>                            source="./local-path")
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
            Entity key (store://...) or entity name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Model
            Object instance.

        Examples
        --------
        Using entity key:
        >>> obj = project.get_model("store://my-model-key")

        Using entity name:
        >>> obj = project.get_model("my-model-name"
        >>>                            entity_id="my-model-id")
        """
        obj = get_model(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            **kwargs,
        )
        self.refresh()
        return obj

    def get_model_versions(
        self,
        identifier: str,
        **kwargs,
    ) -> list[Model]:
        """
        Get object versions from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[Model]
            List of object instances.

        Examples
        --------
        Using entity key:
        >>> obj = project.get_model_versions("store://my-model-key")

        Using entity name:
        >>> obj = project.get_model_versions("my-model-name")
        """
        return get_model_versions(identifier, project=self.name, **kwargs)

    def list_models(self, **kwargs) -> list[Model]:
        """
        List all latest version objects from backend.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[Model]
            List of object instances.

        Examples
        --------
        >>> objs = project.list_models()
        """
        return list_models(self.name, **kwargs)

    def import_model(
        self,
        file: str,
        **kwargs,
    ) -> Model:
        """
        Import object from a YAML file.

        Parameters
        ----------
        file : str
            Path to YAML file.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Model
            Object instance.

        Examples
        --------
        >>> obj = project.import_model("my-model.yaml")
        """
        return import_model(file, **kwargs)

    def update_model(self, entity: Model) -> Model:
        """
        Update object. Note that object spec are immutable.

        Parameters
        ----------
        entity : Model
            Object to update.

        Returns
        -------
        Model
            Entity updated.

        Examples
        --------
        >>> obj = project.update_model(obj)
        """
        if entity.project != self.name:
            raise ValueError(f"Entity {entity.name} is not in project {self.name}.")
        return update_model(entity)

    def delete_model(
        self,
        identifier: str,
        entity_id: str | None = None,
        delete_all_versions: bool = False,
        **kwargs,
    ) -> None:
        """
        Delete object from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        entity_id : str
            Entity ID.
        delete_all_versions : bool
            Delete all versions of the named entity. If True, use entity name instead of entity key as identifier.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.

        Examples
        --------
        If delete_all_versions is False:
        >>> project.delete_model("store://my-model-key")

        Otherwise:
        >>> project.delete_model("my-model-name",
        >>>                         project="my-project",
        >>>                         delete_all_versions=True)
        """
        delete_model(
            identifier=identifier,
            project=self.name,
            entity_id=entity_id,
            delete_all_versions=delete_all_versions,
            **kwargs,
        )
        self.refresh()
