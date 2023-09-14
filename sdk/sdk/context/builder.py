"""
Context builder module.
"""
from __future__ import annotations

import typing

from sdk.context.context import Context

if typing.TYPE_CHECKING:
    from sdk.entities.project.entity import Project


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
        if project_object.name not in self._instances:
            self._instances[project_object.name] = Context(project_object)

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
