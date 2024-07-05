from __future__ import annotations

import typing

from digitalhub_core.entities._builders.metadata import build_metadata
from digitalhub_core.entities._builders.spec import build_spec
from digitalhub_core.entities._builders.status import build_status
from digitalhub_core.utils.env_utils import get_s3_bucket
from digitalhub_core.utils.file_utils import get_file_name
from digitalhub_core.utils.generic_utils import build_uuid
from digitalhub_data.entities.projects.entity import CTX_ENTITIES, FUNC_MAP, ProjectData
from digitalhub_ml.entities.entity_types import EntityTypes
from digitalhub_ml.entities.models.crud import create_model_from_dict, delete_model, get_model, list_models, new_model

if typing.TYPE_CHECKING:
    from digitalhub_ml.entities.models.entity import Model

MODELS = EntityTypes.MODELS.value
CTX_ENTITIES.append(MODELS)
FUNC_MAP[MODELS] = create_model_from_dict


class ProjectMl(ProjectData):
    """
    ProjectMl class.
    """

    #############################
    #  Models
    #############################

    def new_model(self, **kwargs) -> Model:
        """
        Create a Model.

        Parameters
        ----------
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        Model
            Object instance.
        """
        kwargs["project"] = self.name
        kwargs["kind"] = "model"
        obj = new_model(**kwargs)
        self._add_object(obj, MODELS)
        return obj

    def get_model(self, entity_name: str | None = None, entity_id: str | None = None, **kwargs) -> Model:
        """
        Get object from backend.

        Parameters
        ----------
        entity_name : str
            Entity name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        Model
            Instance of Model class.
        """
        obj = get_model(self.name, entity_name=entity_name, entity_id=entity_id, **kwargs)
        self._add_object(obj, MODELS)
        return obj

    def delete_model(self, entity_name: str | None = None, entity_id: str | None = None, **kwargs) -> None:
        """
        Delete a Model from project.

        Parameters
        ----------
        entity_name : str
            Entity name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        delete_model(self.name, entity_name=entity_name, entity_id=entity_id, **kwargs)
        self._delete_object(MODELS, entity_name, entity_id)

    def set_model(self, model: Model) -> None:
        """
        Set a Model.

        Parameters
        ----------
        model : Model
            Model to set.

        Returns
        -------
        None
        """
        self._add_object(model, MODELS)

    def list_models(self, **kwargs) -> list[dict]:
        """
        List models associated with the project.

        Parameters
        ----------
        **kwargs : dict
            Filters to apply to the list. Shold be params={"filter": "value"}.

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
        path: str | None = None,
        source_path: str | None = None,
        **kwargs,
    ) -> Model:
        """
        Log an model to the project.

        Parameters
        ----------
        name : str
            Name that identifies the object.
        kind : str
            Kind of the model.
        path : str
            Destination path of the model.
        source_path : str
            Model location on local machine.
        **kwargs : dict
            New model parameters.

        Returns
        -------
        Model
            Instance of Model class.
        """
        if path is None:
            if source_path is None:
                raise Exception("Either path or source_path must be provided.")

            # Build path if not provided from source filename
            filename = get_file_name(source_path)
            uuid = build_uuid()
            kwargs["uuid"] = uuid
            path = f"s3://{get_s3_bucket()}/{self.name}/{EntityTypes.MODELS.value}/{uuid}/{filename}"

        model = new_model(project=self.name, name=name, kind=kind, path=path, **kwargs)
        model.upload(source_path)
        return model

    @staticmethod
    def _parse_dict(obj: dict, validate: bool = True) -> dict:
        """
        Get dictionary and parse it to a valid entity dictionary.

        Parameters
        ----------
        entity : str
            Entity type.
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        # Override methods to search in digitalhub_ml
        name = obj.get("name")
        kind = obj.get("kind")
        metadata = build_metadata(kind, **obj.get("metadata", {}))
        spec = build_spec(kind, validate=validate, **obj.get("spec", {}))
        status = build_status(kind, **obj.get("status", {}))
        user = obj.get("user")
        local = obj.get("local", False)
        return {
            "name": name,
            "kind": kind,
            "metadata": metadata,
            "spec": spec,
            "status": status,
            "user": user,
            "local": local,
        }


def project_from_parameters(
    name: str,
    kind: str,
    description: str | None = None,
    source: str | None = None,
    labels: list[str] | None = None,
    local: bool = False,
    context: str | None = None,
    **kwargs,
) -> ProjectData:
    """
    Create project.

    Parameters
    ----------
    name : str
        Name that identifies the object.
    kind : str
        Kind of the object.
    description : str
        Description of the object.
    source : str
        Remote git source for object.
    labels : list[str]
        List of labels.
    local : bool
        Flag to determine if object will be exported to backend.
    context : str
        The context of the project.
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    ProjectData
        ProjectData object.
    """
    spec = build_spec(
        kind,
        context=context,
        **kwargs,
    )
    metadata = build_metadata(
        kind,
        project=name,
        name=name,
        description=description,
        labels=labels,
        source=source,
    )
    status = build_status(kind)
    return ProjectMl(
        name=name,
        kind=kind,
        metadata=metadata,
        spec=spec,
        status=status,
        local=local,
    )


def project_from_dict(obj: dict) -> ProjectData:
    """
    Create project from dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    ProjectData
        ProjectData object.
    """
    return ProjectMl.from_dict(obj)
