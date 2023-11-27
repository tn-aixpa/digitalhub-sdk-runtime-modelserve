"""
Context builder module.
"""
from __future__ import annotations

import typing

from digitalhub_core.context.context import Context

if typing.TYPE_CHECKING:
    from digitalhub_core.entities.projects.entity import Project


class ContextBuilder:
    """
    The context builder. It implements the builder pattern to create a context instance.
    It allows to use multiple projects at the same time.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self._instances: dict[str, Context] = {}

    def build(self, project_object: Project) -> None:
        """
        Add a project to the context.

        Parameters
        ----------
        project : Project
            The project to add.

        Returns
        -------
        None
        """
        if project_object.metadata.name not in self._instances:
            self._instances[project_object.metadata.name] = Context(project_object)

    def get(self, project: str) -> Context:
        """
        Get a project from the context.

        Parameters
        ----------
        project : str
            The project name.

        Returns
        -------
        Context
            The project context.
        """
        ctx = self._instances.get(project)
        if ctx is None:
            raise ValueError(f"Context '{project}' not found.")
        return ctx

    def remove(self, project: str) -> None:
        """
        Remove a project from the context.

        Parameters
        ----------
        project : str
            The project name.

        Returns
        -------
        None
        """
        self._instances.pop(project, None)


def set_context(project: Project) -> None:
    """
    Wrapper for ContextBuilder.build().

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
    Wrapper for ContextBuilder.get().

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
    Wrapper for ContextBuilder.remove().

    Parameters
    ----------
    project : str
        Name of the project.

    Returns
    -------
    None
    """
    context_builder.remove(project)


context_builder = ContextBuilder()
