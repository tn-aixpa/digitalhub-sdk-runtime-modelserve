"""
Task metadata module.
"""
from digitalhub_core.entities._base.metadata import Metadata


class TaskMetadata(Metadata):
    """
    A class representing Task metadata.
    """

    def __init__(
        self,
        project: str,
        created: str | None = None,
        updated: str | None = None,
        name: str | None = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        name : str
            Name of the object.

        See Also
        --------
        Metadata.__init__
        """
        super().__init__(project, created, updated)
        self.name = name
