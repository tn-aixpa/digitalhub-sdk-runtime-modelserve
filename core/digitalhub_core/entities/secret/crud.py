from __future__ import annotations

import typing

from digitalhub_core.context.builder import check_context
from digitalhub_core.entities._base.crud import (
    delete_entity_api_ctx,
    list_entity_api_ctx,
    read_entity_api_ctx,
    read_entity_api_ctx_versions,
)
from digitalhub_core.entities.entity_types import EntityTypes
from digitalhub_core.entities.secret.builder import secret_from_dict, secret_from_parameters
from digitalhub_core.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.secret.entity import Secret


ENTITY_TYPE = EntityTypes.SECRET.value


def new_secret(
    project: str,
    name: str,
    uuid: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    embedded: bool = True,
    secret_value: str | None = None,
    **kwargs,
) -> Secret:
    """
    Create a new object.

    Parameters
    ----------
    project : str
        Project name.
    name : str
        Object name.
    uuid : str
        ID of the object (UUID4, e.g. 40f25c4b-d26b-4221-b048-9527aff291e2).
    description : str
        Description of the object (human readable).
    labels : list[str]
        List of labels.
    embedded : bool
        Flag to determine if object spec must be embedded in project spec.
    secret_value : str
        Value of the secret.
    **kwargs : dict
        Spec keyword arguments.

    Returns
    -------
    Secret
        Object instance.

    Examples
    --------
    >>> obj = new_secret(project="my-project",
    >>>                  name="my-secret",
    >>>                  secret_value="my-secret-value")
    """
    check_context(project)

    if secret_value is None:
        raise ValueError("secret_value must be provided.")

    obj = secret_from_parameters(
        project=project,
        name=name,
        kind="secret",
        uuid=uuid,
        description=description,
        labels=labels,
        embedded=embedded,
        **kwargs,
    )
    obj.save()
    obj.set_secret_value(value=secret_value)
    return obj


def get_secret(
    identifier: str,
    project: str | None = None,
    entity_id: str | None = None,
    **kwargs,
) -> Secret:
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
    Secret
        Object instance.

    Examples
    --------
    Using entity key:
    >>> obj = get_secret("store://my-secret-key")

    Using entity name:
    >>> obj = get_secret("my-secret-name"
    >>>                  project="my-project",
    >>>                  entity_id="my-secret-id")
    """
    obj = read_entity_api_ctx(
        identifier,
        ENTITY_TYPE,
        project=project,
        entity_id=entity_id,
        **kwargs,
    )
    return secret_from_dict(obj)


def get_secret_versions(
    identifier: str,
    project: str | None = None,
    **kwargs,
) -> list[Secret]:
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
    list[Secret]
        List of object instances.

    Examples
    --------
    Using entity key:
    >>> objs = get_secret_versions("store://my-secret-key")

    Using entity name:
    >>> objs = get_secret_versions("my-secret-name",
    >>>                            project="my-project")
    """
    obj = read_entity_api_ctx_versions(
        identifier,
        entity_type=ENTITY_TYPE,
        project=project,
        **kwargs,
    )
    return [secret_from_dict(o) for o in obj]


def list_secrets(project: str, **kwargs) -> list[Secret]:
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
    list[Secret]
        List of object instances.

    Examples
    --------
    >>> objs = list_secrets(project="my-project")
    """
    objs = list_entity_api_ctx(
        project=project,
        entity_type=ENTITY_TYPE,
        **kwargs,
    )
    return [secret_from_dict(obj) for obj in objs]


def import_secret(file: str) -> Secret:
    """
    Import object from a YAML file.

    Parameters
    ----------
    file : str
        Path to YAML file.

    Returns
    -------
    Secret
        Object instance.

    Examples
    --------
    >>> obj = import_secret("my-secret.yaml")
    """
    obj: dict = read_yaml(file)
    return secret_from_dict(obj)


def update_secret(entity: Secret) -> Secret:
    """
    Update object. Note that object spec are immutable.

    Parameters
    ----------
    entity : Secret
        Object to update.

    Returns
    -------
    Secret
        Entity updated.

    Examples
    --------
    >>> obj = update_secret(obj)
    """
    return entity.save(update=True)


def delete_secret(
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
    >>> obj = delete_secret("store://my-secret-key")

    Otherwise:
    >>> obj = delete_secret("my-secret-name"
    >>>                     project="my-project",
    >>>                     delete_all_versions=True)
    """
    return delete_entity_api_ctx(
        identifier=identifier,
        entity_type=ENTITY_TYPE,
        project=project,
        entity_id=entity_id,
        delete_all_versions=delete_all_versions,
        **kwargs,
    )
