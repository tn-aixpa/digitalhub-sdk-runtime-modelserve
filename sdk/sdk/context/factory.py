"""
Context factory module.
"""
from __future__ import annotations

import typing

from sdk.context.builder import ContextBuilder

if typing.TYPE_CHECKING:
    from sdk.context.context import Context
    from sdk.entities.project.entity import Project


context_builder = ContextBuilder()


def set_context(project: Project) -> None:
    """
    Set current context to the given project.

    Parameters
    ----------
    project : Project
        The project object used to set the current context.

    Returns
    -------
    None
    """
    context_builder.build(project)


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
    return context_builder.get(project)


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
    context_builder.remove(project)
