from __future__ import annotations

import typing

from digitalhub.client.api import build_client, get_client
from digitalhub.context.api import check_context
from digitalhub.entities._base.crud.api_utils import (
    delete_entity_api_ctx,
    list_entity_api_ctx,
    read_entity_api_base,
    read_entity_api_ctx,
    read_entity_api_ctx_versions,
    search_api,
)
from digitalhub.entities._commons.enums import EntityTypes
from digitalhub.entities._commons.utils import get_project_from_key
from digitalhub.factory.api import build_entity_from_dict, build_entity_from_params
from digitalhub.utils.exceptions import ContextError, EntityAlreadyExistsError, EntityError, EntityNotExistsError
from digitalhub.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.context.entity import ContextEntity
    from digitalhub.entities._base.executable.entity import ExecutableEntity
    from digitalhub.entities._base.material.entity import MaterialEntity
    from digitalhub.entities._base.unversioned.entity import UnversionedEntity
    from digitalhub.entities._base.versioned.entity import VersionedEntity


def _check_context(project: str) -> None:
    """
    Check if the given project is in the context.
    Otherwise try to get the project from remote.

    Parameters
    ----------
    project : str
        Project name.

    Returns
    -------
    None
    """
    try:
        check_context(project)
    except ContextError:
        try:
            build_client()
            client = get_client()
            obj = read_entity_api_base(client, EntityTypes.PROJECT.value, project)
            build_entity_from_dict(obj)
        except EntityNotExistsError:
            raise ContextError(f"Project '{project}' not found.")


def _check_project_from_identifier(identifier: str, project: str | None = None) -> None:
    """
    Check if the given project is in the context.
    Otherwise try to get the project from remote.

    Parameters
    ----------
    identifier : str
        Entity key (store://...) or entity name.
    project : str
        Project name.

    Returns
    -------
    None
    """
    if not identifier.startswith("store://"):
        if project is None:
            raise EntityError("Specify project if you do not specify entity key.")

    else:
        project = get_project_from_key(identifier)

    _check_context(project)


def new_context_entity(**kwargs) -> ContextEntity:
    """
    Create a new object.

    Parameters
    ----------
    project : str
        Project name.
    kind : str
        Kind the object.
    uuid : str
        ID of the object.
    description : str
        Description of the object (human readable).
    labels : list[str]
        List of labels.
    embedded : bool
        Flag to determine if object spec must be embedded in project spec.

    Returns
    -------
    ContextEntity
        Object instance.
    """
    _check_context(kwargs["project"])
    obj = build_entity_from_params(**kwargs)
    obj.save()
    return obj


def get_versioned_entity(
    identifier: str,
    entity_type: str | None = None,
    project: str | None = None,
    entity_id: str | None = None,
    **kwargs,
) -> VersionedEntity:
    """
    Get object from backend.

    Parameters
    ----------
    identifier : str
        Entity key (store://...) or entity name.
    entity_type : str
        Entity type.
    project : str
        Project name.
    entity_id : str
        Entity ID.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    VersionedEntity
        Object instance.
    """
    _check_project_from_identifier(identifier, project)
    obj = read_entity_api_ctx(
        identifier,
        entity_type=entity_type,
        project=project,
        entity_id=entity_id,
        **kwargs,
    )
    return build_entity_from_dict(obj)


def get_unversioned_entity(
    identifier: str,
    entity_type: str | None = None,
    project: str | None = None,
    **kwargs,
) -> UnversionedEntity:
    """
    Get object from backend.

    Parameters
    ----------
    entity_type : str
        Entity type.
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
    UnversionedEntity
        Object instance.
    """
    _check_project_from_identifier(identifier, project)

    obj = read_entity_api_ctx(
        identifier,
        entity_type=entity_type,
        project=project,
        **kwargs,
    )
    return build_entity_from_dict(obj)


def get_material_entity(
    identifier: str,
    entity_type: str | None = None,
    project: str | None = None,
    entity_id: str | None = None,
    **kwargs,
) -> MaterialEntity:
    """
    Get object from backend.

    Parameters
    ----------
    identifier : str
        Entity key (store://...) or entity name.
    entity_type : str
        Entity type.
    project : str
        Project name.
    entity_id : str
        Entity ID.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    MaterialEntity
        Object instance.
    """
    obj: MaterialEntity = get_versioned_entity(
        identifier,
        entity_type=entity_type,
        project=project,
        entity_id=entity_id,
        **kwargs,
    )
    obj._get_files_info()
    return obj


def get_context_entity_versions(
    identifier: str,
    entity_type: str | None = None,
    project: str | None = None,
    **kwargs,
) -> list[ContextEntity]:
    """
    Get object versions from backend.

    Parameters
    ----------
    identifier : str
        Entity key (store://...) or entity name.
    entity_type : str
        Entity type.
    project : str
        Project name.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    list[ContextEntity]
        List of object instances.
    """
    _check_project_from_identifier(identifier, project)
    obj = read_entity_api_ctx_versions(
        identifier,
        entity_type=entity_type,
        project=project,
        **kwargs,
    )
    return [build_entity_from_dict(o) for o in obj]


def get_material_entity_versions(
    identifier: str,
    entity_type: str | None = None,
    project: str | None = None,
    **kwargs,
) -> list[MaterialEntity]:
    """
    Get object versions from backend.

    Parameters
    ----------
    identifier : str
        Entity key (store://...) or entity name.
    entity_type : str
        Entity type.
    project : str
        Project name.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    list[MaterialEntity]
        List of object instances.
    """
    _check_project_from_identifier(identifier, project)
    objs = read_entity_api_ctx_versions(
        identifier,
        entity_type=entity_type,
        project=project,
        **kwargs,
    )
    objects = []
    for o in objs:
        entity: MaterialEntity = build_entity_from_dict(o)
        entity._get_files_info()
        objects.append(entity)
    return objects


def list_context_entities(project: str, entity_type: str, **kwargs) -> list[ContextEntity]:
    """
    List all latest version objects from backend.

    Parameters
    ----------
    project : str
        Project name.
    entity_type : str
        Entity type.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    list[ContextEntity]
        List of object instances.
    """
    _check_context(project)
    objs = list_entity_api_ctx(
        project=project,
        entity_type=entity_type,
        **kwargs,
    )
    return [build_entity_from_dict(obj) for obj in objs]


def list_material_entities(
    project: str,
    entity_type: str,
    **kwargs,
) -> list[MaterialEntity]:
    """
    List all latest version objects from backend.

    Parameters
    ----------
    project : str
        Project name.
    entity_type : str
        Entity type.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    list[MaterialEntity]
        List of object instances.
    """
    _check_context(project)
    objs = list_entity_api_ctx(
        project=project,
        entity_type=entity_type,
        **kwargs,
    )
    objects = []
    for o in objs:
        entity: MaterialEntity = build_entity_from_dict(o)
        entity._get_files_info()
        objects.append(entity)
    return objects


def import_context_entity(file: str) -> ContextEntity:
    """
    Import object from a YAML file and create a new object into the backend.

    Parameters
    ----------
    file : str
        Path to YAML file.

    Returns
    -------
    ContextEntity
        Object instance.
    """
    dict_obj: dict = read_yaml(file)

    _check_context(dict_obj["project"])

    obj = build_entity_from_dict(dict_obj)
    try:
        obj.save()
    except EntityAlreadyExistsError:
        raise EntityError(f"Entity {obj.name} already exists. If you want to update it, use load instead.")
    return obj


def import_executable_entity(file: str) -> ExecutableEntity:
    """
    Import object from a YAML file and create a new object into the backend.

    Parameters
    ----------
    file : str
        Path to YAML file.

    Returns
    -------
    ExecutableEntity
        Object instance.
    """
    dict_obj: dict | list[dict] = read_yaml(file)
    if isinstance(dict_obj, list):
        exec_dict = dict_obj[0]
        tsk_dicts = dict_obj[1:]
    else:
        exec_dict = dict_obj
        tsk_dicts = []

    _check_context(exec_dict["project"])

    obj: ExecutableEntity = build_entity_from_dict(exec_dict)

    obj.import_tasks(tsk_dicts)

    try:
        obj.save()
    except EntityAlreadyExistsError:
        raise EntityError(f"Entity {obj.name} already exists. If you want to update it, use load instead.")
    return obj


def load_context_entity(file: str) -> ContextEntity:
    """
    Load object from a YAML file and update an existing object into the backend.

    Parameters
    ----------
    file : str
        Path to YAML file.

    Returns
    -------
    ContextEntity
        Object instance.
    """
    dict_obj: dict = read_yaml(file)

    _check_context(dict_obj["project"])

    obj = build_entity_from_dict(dict_obj)
    try:
        obj.save(update=True)
    except EntityNotExistsError:
        obj.save()
    return obj


def load_executable_entity(file: str) -> ExecutableEntity:
    """
    Load object from a YAML file and update an existing object into the backend.

    Parameters
    ----------
    file : str
        Path to YAML file.

    Returns
    -------
    ExecutableEntity
        Object instance.
    """
    dict_obj: dict | list[dict] = read_yaml(file)
    if isinstance(dict_obj, list):
        exec_dict = dict_obj[0]
        tsk_dicts = dict_obj[1:]
    else:
        exec_dict = dict_obj
        tsk_dicts = []

    _check_context(exec_dict["project"])

    obj: ExecutableEntity = build_entity_from_dict(exec_dict)

    obj.import_tasks(tsk_dicts)

    try:
        obj.save(update=True)
    except EntityNotExistsError:
        obj.save()
    return obj


def search_entity(
    project: str,
    query: str | None = None,
    entity_types: list[str] | None = None,
    name: str | None = None,
    kind: str | None = None,
    created: str | None = None,
    updated: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    **kwargs,
) -> list[ContextEntity]:
    """
    Search objects from backend.

    Parameters
    ----------
    project : str
        Project name.
    query : str
        Search query.
    entity_types : list[str]
        Entity types.
    name : str
        Entity name.
    kind : str
        Entity kind.
    created : str
        Entity creation date.
    updated : str
        Entity update date.
    description : str
        Entity description.
    labels : list[str]
        Entity labels.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    list[ContextEntity]
        List of object instances.
    """
    _check_context(project)

    if "params" not in kwargs:
        kwargs["params"] = {}

    # Add search query
    if query is not None:
        kwargs["params"]["q"] = query

    # Add search filters
    fq = []

    # Entity types
    if entity_types is not None:
        if len(entity_types) == 1:
            entity_types = entity_types[0]
        else:
            entity_types = " OR ".join(entity_types)
        fq.append(f"type:({entity_types})")

    # Name
    if name is not None:
        fq.append(f'metadata.name:"{name}"')

    # Kind
    if kind is not None:
        fq.append(f'kind:"{kind}"')

    # Time
    created = created if created is not None else "*"
    updated = updated if updated is not None else "*"
    fq.append(f"metadata.updated:[{created} TO {updated}]")

    # Description
    if description is not None:
        fq.append(f'metadata.description:"{description}"')

    # Labels
    if labels is not None:
        if len(labels) == 1:
            labels = labels[0]
        else:
            labels = " AND ".join(labels)
        fq.append(f"metadata.labels:({labels})")

    # Add filters
    kwargs["params"]["fq"] = fq

    objs = search_api(
        project=project,
        **kwargs,
    )
    return objs
    return [build_entity_from_dict(obj) for obj in objs]


def delete_entity(
    identifier: str,
    entity_type: str | None = None,
    project: str | None = None,
    entity_id: str | None = None,
    delete_all_versions: bool = False,
    cascade: bool = True,
    **kwargs,
) -> dict:
    """
    Delete object from backend.

    Parameters
    ----------
    identifier : str
        Entity key (store://...) or entity name.
    entity_type : str
        Entity type.
    project : str
        Project name.
    entity_id : str
        Entity ID.
    delete_all_versions : bool
        Delete all versions of the named entity. If True, use entity name instead of entity key as identifier.
    cascade : bool
        Cascade delete.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    dict
        Response from backend.
    """
    _check_project_from_identifier(identifier, project)
    return delete_entity_api_ctx(
        identifier=identifier,
        entity_type=entity_type,
        project=project,
        entity_id=entity_id,
        delete_all_versions=delete_all_versions,
        cascade=cascade,
        **kwargs,
    )
