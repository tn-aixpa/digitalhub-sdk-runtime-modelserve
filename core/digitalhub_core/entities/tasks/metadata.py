"""
Task metadata module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.metadata import Metadata


class TaskMetadata(Metadata):
    """
    A class representing Task metadata.
    """

    def __init__(
        self,
        project: str | None = None,
        name: str | None = None,
        source: str | None = None,
        lables: list[str] | None = None,
        created: str | None = None,
        updated: str | None = None,
        **kwargs,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        project : str
            Project name.
        name : str
            Name (UUID) of the object.

        See Also
        --------
        Metadata.__init__
        """
        super().__init__(source, lables, created, updated)
        self.project = project
        self.name = name
