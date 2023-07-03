"""
Context builder module.
"""
from __future__ import annotations

import typing

from sdk.entities.context.entity import Context

if typing.TYPE_CHECKING:
    from sdk.entities.project.entity import Project


class ContextBuilder:
    """
    The context builder. It implements the builder pattern to create a context instance.
    It allows to use multiple projects at the same time.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._instances = {}

    def build(self, project: Project) -> None:
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
        if project.name not in self._instances:
            self._instances[project.name] = Context(project)

    def get(self, project_name: str) -> Context:
        """
        Get a project from the context.

        Parameters
        ----------
        project_name : str
            The project name.

        Returns
        -------
        Context
            The project context.
        """
        ctx = self._instances.get(project_name)
        if ctx is None:
            raise ValueError(f"Context '{project_name}' not found.")
        return ctx

    def remove(self, project_name: str) -> None:
        """
        Remove a project from the context.

        Parameters
        ----------
        project_name : str
            The project name.

        Returns
        -------
        None
        """
        self._instances.pop(project_name, None)
