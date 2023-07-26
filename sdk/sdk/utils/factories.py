"""
Factory module.
"""
from __future__ import annotations

import typing

from sdk.client.builder import ClientBuilder
from sdk.entities.context.builder import ContextBuilder
from sdk.store.builder import StoreBuilder

if typing.TYPE_CHECKING:
    from sdk.client.client import Client
    from sdk.entities.context.entity import Context
    from sdk.entities.project.entity import Project
    from sdk.store.models import StoreConfig
    from sdk.store.objects.base import Store


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
    Set a new store instance with the given configuration.

    Parameters
    ----------
    store_cfg : StoreConfig
        Store configuration.

    Returns
    -------
    None
    """
    store_builder.build(store_cfg=store_cfg)


def get_store(store_name: str) -> Store:
    """
    Get store instance by name.

    Parameters
    ---------
    store_name : str
        Store name.

    Returns
    -------
    Store
        Store instance.
    """
    return store_builder.get(store_name=store_name)


def get_default_store() -> Store:
    """
    Get the default store instance. The default store is the one that
    can persist artifacts and dataitems.

    Returns
    -------
    Store
        Default store instance.
    """
    return store_builder.default()


####################
# Context
####################


def set_context(project_object: Project) -> None:
    """
    Set current context to the given project.

    Parameters
    ----------
    project_object : Project
        The project object used to set the current context.

    Returns
    -------
    None
    """
    context_builder.build(project_object=project_object)


def get_context(project: str) -> Context:
    """
    Get specific context by project name.

    Parameters
    ----------
    project : str
        Name of the project.

    Returns
    -------
    Context
        The context for the given project name.
    """
    return context_builder.get(project=project)


def delete_context(project: str) -> None:
    """
    Delete the context for the given project name.

    Parameters
    ----------
    project : str
        Name of the project.

    Returns
    -------
    None
    """
    context_builder.remove(project=project)
