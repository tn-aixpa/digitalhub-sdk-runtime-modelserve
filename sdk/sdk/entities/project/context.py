from __future__ import annotations

import typing
from typing import Literal

if typing.TYPE_CHECKING:
    from sdk.entities.project.project import Project


class Context:
    """
    The context for a project.
    """

    def __init__(self, project: Project) -> None:
        """
        Initialize the context.

        Parameters
        ----------

        project : Project
            The project to create the context for.

        Returns
        -------
        None
        """
        self.name = project.name
        self.client = project.client
        self.local = project.local


class ContextBuilder:
    """
    The context builder.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._instances = {}

    def __call__(
        self,
        options: Literal["add", "get", "remove"],
        project: Project = None,
        project_name: str = None,
    ):
        """
        Call method.

        Parameters
        ----------
        options : Literal["add", "get", "remove"]
            The options to call the method with.
        """
        if options == "add":
            if project.name not in self._instances:
                self._instances[project.name] = Context(project)
            return
        if options == "get":
            ctx = self._instances.get(project_name)
            if ctx is None:
                raise ValueError(f"Context '{project_name}' not found.")
            return ctx
        if options == "remove":
            self._instances.pop(project_name, None)
            return
        raise ValueError(f"Invalid option '{options}'.")
