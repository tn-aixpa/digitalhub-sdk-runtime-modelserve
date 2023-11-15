"""
Project metadata module.
"""
from digitalhub_core.entities._base.metadata import Metadata


class ProjectMetadata(Metadata):
    """
    A class representing Project metadata.
    """

    def __init__(
        self,
        project: str,
        created: str | None = None,
        updated: str | None = None,
        name: str | None = None,
        version: str | None = None,
        description: str | None = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        name : str
            Name of the object.
        version : str
            Version of the object.
        description : str
            Description of the entity.

        See Also
        --------
        Metadata.__init__
        """
        super().__init__(project, created, updated)
        self.name = name
        self.version = version
        self.description = description
