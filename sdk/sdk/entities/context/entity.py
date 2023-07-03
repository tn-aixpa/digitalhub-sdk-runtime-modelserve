"""
Context module.
"""
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from sdk.entities.project.entity import Project


class Context:
    """
    The context for a project. It contains the project name, the client and the local store.
    It is a simplified version of the project class, used to avoid circular dependencies.
    The context is created by the context builder.
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
