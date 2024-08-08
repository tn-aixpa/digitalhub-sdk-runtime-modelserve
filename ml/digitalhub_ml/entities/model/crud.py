from __future__ import annotations

import typing
from pathlib import Path

from digitalhub_core.context.builder import check_context
from digitalhub_core.entities._base.crud import (
    delete_entity_api_ctx,
    list_entity_api_ctx,
    read_entity_api_ctx,
    read_entity_api_ctx_versions,
)
from digitalhub_core.entities._builders.uuid import build_uuid
from digitalhub_core.utils.env_utils import get_s3_bucket
from digitalhub_core.utils.io_utils import read_yaml
from digitalhub_ml.entities.entity_types import EntityTypes
from digitalhub_ml.entities.model.builder import model_from_dict, model_from_parameters

if typing.TYPE_CHECKING:
    from digitalhub_ml.entities.model.entity._base import Model


ENTITY_TYPE = EntityTypes.MODEL.value


def create_model(**kwargs) -> Model:
    """
    Create a new Model instance with the specified parameters.

    Parameters
    ----------
    **kwargs : dict
        Keyword arguments.

    Returns
    -------
    Model
        An instance of the created model.
    """
    return model_from_parameters(**kwargs)


def create_model_from_dict(obj: dict) -> Model:
    """
    Create a new Model instance from a dictionary.

    Parameters
    ----------
    obj : dict
        Dictionary to create object from.

    Returns
    -------
    Model
        Model object.
    """
    check_context(obj.get("project"))
    return model_from_dict(obj)


def new_model(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    path: str | None = None,
    framework: str | None = None,
    algorithm: str | None = None,
    **kwargs,
) -> Model:
    """
    Create a new Model instance with the specified parameters.

    Parameters
    ----------
    project : str
        Project name.
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
        If not provided, it's generated.
    framework : str
        Model framework (e.g. 'pytorch').
    algorithm : str
        Model algorithm (e.g. 'resnet').
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    Model
        An instance of the created model.
    """
    obj = create_model(
        project=project,
        name=name,
        kind=kind,
        uuid=uuid,
        description=description,
        labels=labels,
        embedded=embedded,
        path=path,
        framework=framework,
        algorithm=algorithm,
        **kwargs,
    )
    obj.save()
    return obj


def get_model(
    identifier: str,
    project: str | None = None,
    entity_id: str | None = None,
    **kwargs,
) -> Model:
    """
    Get object from backend.

    Parameters
    ----------
    identifier : str
        Entity key or name.
    project : str
        Project name.
    entity_id : str
        Entity ID.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    Model
        Object instance.
    """
    obj = read_entity_api_ctx(
        identifier,
        ENTITY_TYPE,
        project=project,
        entity_id=entity_id,
        **kwargs,
    )
    entity = model_from_dict(obj)
    entity._get_files_info()
    return entity


def get_model_versions(
    identifier: str,
    project: str | None = None,
    **kwargs,
) -> list[Model]:
    """
    Get object versions from backend.

    Parameters
    ----------
    identifier : str
        Entity key or name.
    project : str
        Project name.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    list[Model]
        List of object instances.
    """
    objs = read_entity_api_ctx_versions(
        identifier,
        entity_type=ENTITY_TYPE,
        project=project,
        **kwargs,
    )
    objects = []
    for o in objs:
        entity = model_from_dict(o)
        entity._get_files_info()
        objects.append(entity)
    return objects


def import_model(file: str) -> Model:
    """
    Import an Model object from a file using the specified file path.

    Parameters
    ----------
    file : str
        Path to the file.

    Returns
    -------
    Model
        Object instance.
    """
    obj: dict = read_yaml(file)
    return create_model_from_dict(obj)


def delete_model(
    identifier: str,
    project: str | None = None,
    entity_id: str | None = None,
    delete_all_versions: bool = False,
    **kwargs,
) -> dict:
    """
    Delete object from backend.

    Parameters
    ----------
    identifier : str
        Entity key or name.
    project : str
        Project name.
    entity_id : str
        Entity ID.
    delete_all_versions : bool
        Delete all versions of the named entity.
        Use entity name instead of entity key as identifier.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    dict
        Response from backend.
    """
    return delete_entity_api_ctx(
        identifier=identifier,
        entity_type=ENTITY_TYPE,
        project=project,
        entity_id=entity_id,
        delete_all_versions=delete_all_versions,
        **kwargs,
    )


def update_model(entity: Model) -> Model:
    """
    Update object in backend.

    Parameters
    ----------
    entity : Model
        The object to update.

    Returns
    -------
    Model
        Entity updated.
    """
    return entity.save(update=True)


def list_models(project: str, **kwargs) -> list[Model]:
    """
    List all objects from backend.

    Parameters
    ----------
    project : str
        Project name.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    list[Model]
        List of models.
    """
    objs = list_entity_api_ctx(
        project=project,
        entity_type=ENTITY_TYPE,
        **kwargs,
    )
    objects = []
    for o in objs:
        entity = model_from_dict(o)
        entity._get_files_info()
        objects.append(entity)
    return objects


def log_model(
    project: str,
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
    project : str
        Project name.
    name : str
        Object name.
    kind : str
        Kind the object.
    source : str
        Model location on local machine.
    path : str
        Destination path of the model.
    **kwargs : dict
        New model parameters.

    Returns
    -------
    Model
        Instance of Model class.
    """
    if path is None:
        uuid = build_uuid()
        kwargs["uuid"] = uuid
        path = f"s3://{get_s3_bucket()}/{project}/{ENTITY_TYPE}/{name}/{uuid}"
        if Path(source).is_dir():
            path = f"{path}/"

    obj = new_model(project=project, name=name, kind=kind, path=path, **kwargs)
    obj.upload(source)
    return obj
