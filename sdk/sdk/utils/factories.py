"""
Context utilities.
"""
from __future__ import annotations

import typing

from sdk.client.builder import ClientBuilder
from sdk.entities.context.builder import ContextBuilder
from sdk.store.builder import StoreBuilder

if typing.TYPE_CHECKING:
    from sdk.client.models import Client
    from sdk.entities.context.context import Context
    from sdk.entities.project.project import Project
    from sdk.store.models import Store, StoreConfig


####################
# Builders
####################

client_builder = ClientBuilder()
store_builder = StoreBuilder()
context_builder = ContextBuilder()


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
    return client_builder.build()


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
    store_builder.build(store_cfg=store_cfg)


def get_store(store_name: str) -> Store:
    """
    Get store instance.

    Parameters
    ---------
    store_name : str
        The name of the registered store.

    Returns
    -------
    Store
        The store instance.
    """
    return store_builder.get(store_name=store_name)


def get_default_store() -> Store:
    """
    Get the default writer store instance.

    Returns
    -------
    Store
        The default store instance.
    """
    return store_builder.default()


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
    context_builder.build(project=project)


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
    return context_builder.get(project_name=project_name)


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
    context_builder.remove(project_name=project_name)
