"""
Run metadata module.
"""
from sdk.entities._base.metadata import Metadata


class RunMetadata(Metadata):
    """
    A class representing Run metadata.
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
