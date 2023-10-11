"""
Entity metadata module.
"""
from sdk.entities.base.base import ModelObj
from sdk.utils.generic_utils import get_timestamp


class Metadata(ModelObj):
    """
    A class representing the metadata of an entity.
    """

    def __init__(
        self, project: str, created: str | None = None, updated: str | None = None
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        project : str
            Name of the project.
        created : str
            Created date.
        updated : str
            Updated date.
        """
        self.project = project
        self.created = created if created is not None else get_timestamp()
        self.updated = updated if updated is not None else self.created

    @classmethod
    def from_dict(cls, obj: dict | None = None) -> "Metadata":
        """
        Return entity metadata object from dictionary.

        Parameters
        ----------
        obj : dict
            A dictionary containing the attributes of the entity metadata.

        Returns
        -------
        Metadata
            An entity metadata object.
        """
        obj = obj if obj is not None else {}
        return cls(**obj)
