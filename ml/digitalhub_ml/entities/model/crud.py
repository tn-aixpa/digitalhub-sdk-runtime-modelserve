from __future__ import annotations

import typing

from digitalhub_core.context.builder import check_context
from digitalhub_core.entities._base.crud import (
    delete_entity_api_ctx,
    list_entity_api_ctx,
    read_entity_api_ctx,
    read_entity_api_ctx_versions,
)
from digitalhub_core.entities._builders.uuid import build_uuid
from digitalhub_core.entities.utils import build_log_path_from_source, eval_local_source
from digitalhub_core.utils.io_utils import read_yaml
from digitalhub_ml.entities.entity_types import EntityTypes
from digitalhub_ml.entities.model.builder import model_from_dict, model_from_parameters

if typing.TYPE_CHECKING:
    from digitalhub_ml.entities.model.entity._base import Model


ENTITY_TYPE = EntityTypes.MODEL.value


def new_model(
    project: str,
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
    project : str
        Project name.
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
    >>> obj = new_model(project="my-project",
    >>>                    name="my-model",
    >>>                    kind="model",
    >>>                    path="s3://my-bucket/my-key")
    """
    check_context(project)
    obj = model_from_parameters(
        project=project,
        name=name,
        kind=kind,
        uuid=uuid,
        description=description,
        labels=labels,
        embedded=embedded,
        path=path,
        **kwargs,
    )
    obj.save()
    return obj


def log_model(
    project: str,
    name: str,
    kind: str,
    source: list[str] | str,
    path: str | None = None,
    **kwargs,
) -> Model:
    """
    Create and upload an object.

    Parameters
    ----------
    project : str
        Project name.
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
    >>> obj = log_model(project="my-project",
    >>>                 name="my-model",
    >>>                 kind="model",
    >>>                 source="./local-path")
    """
    eval_local_source(source)

    if path is None:
        uuid = build_uuid()
        kwargs["uuid"] = uuid
        path = build_log_path_from_source(project, ENTITY_TYPE, name, uuid, source)

    obj = new_model(project=project, name=name, kind=kind, path=path, **kwargs)
    obj.upload(source)
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
        Entity key (store://...) or entity name.
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

    Examples
    --------
    Using entity key:
    >>> obj = get_model("store://my-model-key")

    Using entity name:
    >>> obj = get_model("my-model-name"
    >>>                 project="my-project",
    >>>                 entity_id="my-model-id")
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
        Entity key (store://...) or entity name.
    project : str
        Project name.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    list[Model]
        List of object instances.

    Examples
    --------
    Using entity key:
    >>> objs = get_model_versions("store://my-model-key")

    Using entity name:
    >>> objs = get_model_versions("my-model-name",
    >>>                           project="my-project")
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


def list_models(project: str, **kwargs) -> list[Model]:
    """
    List all latest version objects from backend.

    Parameters
    ----------
    project : str
        Project name.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    list[Model]
        List of object instances.

    Examples
    --------
    >>> objs = list_models(project="my-project")
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


def import_model(file: str) -> Model:
    """
    Import object from a YAML file.

    Parameters
    ----------
    file : str
        Path to YAML file.

    Returns
    -------
    Model
        Object instance.

    Examples
    --------
    >>> obj = import_model("my-model.yaml")
    """
    obj: dict = read_yaml(file)
    return model_from_dict(obj)


def update_model(entity: Model) -> Model:
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
    >>> obj = get_model("store://my-model-key")
    """
    return entity.save(update=True)


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
        Entity key (store://...) or entity name.
    project : str
        Project name.
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
    >>> obj = delete_model("store://my-model-key")

    Otherwise:
    >>> obj = delete_model("my-model-name",
    >>>                    project="my-project",
    >>>                    delete_all_versions=True)
    """
    return delete_entity_api_ctx(
        identifier=identifier,
        entity_type=ENTITY_TYPE,
        project=project,
        entity_id=entity_id,
        delete_all_versions=delete_all_versions,
        **kwargs,
    )
