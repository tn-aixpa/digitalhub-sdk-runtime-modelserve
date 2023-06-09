"""
Context utilities.
"""
from __future__ import annotations

import typing

from sdk.utils.factories import factory

if typing.TYPE_CHECKING:
    from sdk.client.models import Client
    from sdk.entities.project.context import Context
    from sdk.entities.project.project import Project
    from sdk.store.models import Store, StoreConfig


####################
# Client
####################


def get_client() -> Client:
    """
    Get the client instance.

    Returns
    -------
    Client
        The client instance.
    """
    return factory.create("client")


####################
# Store
####################


def set_store(store_cfg: StoreConfig) -> None:
    """
    Set the store instance.

    Parameters
    ----------
    store_cfg : StoreConfig
        The store configuration.

    Returns
    -------
    None
    """
    factory.create("store", store_cfg=store_cfg)


def get_store() -> Store:
    """
    Get the store instance.

    Returns
    -------
    Store
        The store instance.
    """
    return factory.create("store")


####################
# Context
####################


def set_context(project: Project) -> None:
    """
    Set the current context to the given project.

    Parameters
    ----------
    project : Project
        The project to set as the current context.

    Returns
    -------
    None

    """
    factory.create("context", options="add", project=project)


def get_context(project_name: str) -> Context:
    """
    Get the specific context.

    Parameters
    ----------
    project_name : str
        The name of the project to get the context for.

    Returns
    -------
    Context
        The context for the given project name.

    """
    return factory.create("context", options="get", project_name=project_name)


def delete_context(project_name: str) -> None:
    """
    Delete the context for the given project name.

    Parameters
    ----------
    project_name : str
        The name of the project to delete the context for.

    Returns
    -------
    None
    """
    factory.create("context", options="remove", project_name=project_name)
