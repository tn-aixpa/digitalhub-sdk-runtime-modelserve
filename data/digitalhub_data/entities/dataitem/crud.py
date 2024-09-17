from __future__ import annotations

import typing
from pathlib import Path
from typing import Any

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
from digitalhub_core.utils.uri_utils import check_local_path
from digitalhub_data.entities.dataitem.builder import dataitem_from_dict, dataitem_from_parameters
from digitalhub_data.entities.entity_types import EntityTypes
from digitalhub_data.readers.builder import get_reader_by_object

if typing.TYPE_CHECKING:
    from digitalhub_data.entities.dataitem.entity._base import Dataitem


ENTITY_TYPE = EntityTypes.DATAITEM.value


def new_dataitem(
    project: str,
    name: str,
    kind: str,
    uuid: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    path: str | None = None,
    **kwargs,
) -> Dataitem:
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
    Dataitem
        Object instance.

    Examples
    --------
    >>> obj = new_dataitem(project="my-project",
    >>>                    name="my-dataitem",
    >>>                    kind="dataitem",
    >>>                    path="s3://my-bucket/my-key")
    """
    check_context(project)
    obj = dataitem_from_parameters(
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


def log_dataitem(
    project: str,
    name: str,
    kind: str,
    source: list[str] | str | None = None,
    data: Any | None = None,
    extension: str | None = None,
    path: str | None = None,
    **kwargs,
) -> Dataitem:
    """
    Log a dataitem to the project.

    Parameters
    ----------
    project : str
        Project name.
    name : str
        Object name.
    kind : str
        Kind the object.
    source : str
        Dataitem location on local path.
    data : Any
        Dataframe to log. Alternative to source.
    extension : str
        Extension of the output dataframe.
    path : str
        Destination path of the dataitem. If not provided, it's generated.
    **kwargs : dict
        New dataitem spec parameters.

    Returns
    -------
    Dataitem
        Object instance.

    Examples
    --------
    >>> obj = log_dataitem(project="my-project",
    >>>                    name="my-dataitem",
    >>>                    kind="table",
    >>>                    data=df)
    """
    if (source is None) == (data is None):
        raise ValueError("You must provide source or data.")

    # Case where source is provided
    if source is not None:
        if isinstance(source, list):
            source_is_local = all(check_local_path(s) for s in source)
            for s in source:
                if Path(s).is_dir():
                    raise ValueError(f"Invalid source path: {s}. List of paths must be list of files, not directories.")
        else:
            source_is_local = check_local_path(source)

        if path is not None:
            if not source_is_local:
                raise ValueError("If you provide a path, you must use a local path as source.")
        else:
            if source_is_local:
                uuid = build_uuid()
                kwargs["uuid"] = uuid
                path = f"s3://{get_s3_bucket()}/{project}/{ENTITY_TYPE}/{name}/{uuid}"

                if isinstance(source, list) or Path(source).is_dir():
                    path = f"{path}/"
                elif Path(source).is_file():
                    path = f"{path}/{Path(source).name}"
                else:
                    raise ValueError(f"Invalid source path: {source}")

            else:
                path = source

            obj = new_dataitem(project=project, name=name, kind=kind, path=path, **kwargs)
            if source_is_local:
                obj.upload(source)

    # Case where data is provided
    else:
        if path is None:
            uuid = build_uuid()
            kwargs["uuid"] = uuid
            path = f"s3://{get_s3_bucket()}/{project}/{ENTITY_TYPE}/{name}/{uuid}/data.parquet"

        obj = dataitem_from_parameters(project=project, name=name, kind=kind, path=path, **kwargs)
        if kind == "table":
            obj.write_df(df=data, extension=extension)
            reader = get_reader_by_object(data)
            obj.spec.schema = reader.get_schema(data)
            obj.status.preview = reader.get_preview(data)
            obj.save()

    return obj


def get_dataitem(
    identifier: str,
    project: str | None = None,
    entity_id: str | None = None,
    **kwargs,
) -> Dataitem:
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
    Dataitem
        Object instance.

    Examples
    --------
    Using entity key:
    >>> obj = get_dataitem("store://my-dataitem-key")

    Using entity name:
    >>> obj = get_dataitem("my-dataitem-name"
    >>>                    project="my-project",
    >>>                    entity_id="my-dataitem-id")
    """
    obj = read_entity_api_ctx(
        identifier,
        ENTITY_TYPE,
        project=project,
        entity_id=entity_id,
        **kwargs,
    )
    entity = dataitem_from_dict(obj)
    entity._get_files_info()
    return entity


def get_dataitem_versions(
    identifier: str,
    project: str | None = None,
    **kwargs,
) -> list[Dataitem]:
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
    list[Dataitem]
        List of object instances.

    Examples
    --------
    Using entity key:
    >>> objs = get_dataitem_versions("store://my-dataitem-key")

    Using entity name:
    >>> objs = get_dataitem_versions("my-dataitem-name",
    >>>                              project="my-project")
    """
    objs = read_entity_api_ctx_versions(
        identifier,
        entity_type=ENTITY_TYPE,
        project=project,
        **kwargs,
    )
    objects = []
    for o in objs:
        entity = dataitem_from_dict(o)
        entity._get_files_info()
        objects.append(entity)
    return objects


def list_dataitems(project: str, **kwargs) -> list[Dataitem]:
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
    list[Dataitem]
        List of object instances.

    Examples
    --------
    >>> objs = list_dataitems(project="my-project")
    """
    objs = list_entity_api_ctx(
        project=project,
        entity_type=ENTITY_TYPE,
        **kwargs,
    )
    objects = []
    for o in objs:
        entity = dataitem_from_dict(o)
        entity._get_files_info()
        objects.append(entity)
    return objects


def import_dataitem(file: str) -> Dataitem:
    """
    Import object from a YAML file.

    Parameters
    ----------
    file : str
        Path to YAML file.

    Returns
    -------
    Dataitem
        Object instance.

    Examples
    --------
    >>> obj = import_dataitem("my-dataitem.yaml")
    """
    obj: dict = read_yaml(file)
    return dataitem_from_dict(obj)


def update_dataitem(entity: Dataitem) -> Dataitem:
    """
    Update object. Note that object spec are immutable.

    Parameters
    ----------
    entity : Dataitem
        Object to update.

    Returns
    -------
    Dataitem
        Entity updated.

    Examples
    --------
    >>> obj = update_dataitem(obj)
    """
    return entity.save(update=True)


def delete_dataitem(
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
    >>> obj = delete_dataitem("store://my-dataitem-key")

    Otherwise:
    >>> obj = delete_dataitem("my-dataitem-name",
    >>>                       project="my-project",
    >>>                       delete_all_versions=True)
    """
    return delete_entity_api_ctx(
        identifier=identifier,
        entity_type=ENTITY_TYPE,
        project=project,
        entity_id=entity_id,
        delete_all_versions=delete_all_versions,
        **kwargs,
    )
