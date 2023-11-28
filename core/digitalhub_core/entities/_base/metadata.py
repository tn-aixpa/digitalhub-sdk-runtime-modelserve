"""
Entity metadata module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.base import ModelObj


class Metadata(ModelObj):
    """
    A class representing the metadata of an entity.
    """

    def __init__(
        self,
        source: str | None = None,
        labels: list[str] | None = None,
        created: str | None = str,
        updated: str | None = str,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        source : str
            Source of the entity.
        labels : list[str]
            A list of labels.
        created : str
            Created date.
        updated : str
            Updated date.
        """
        self.source = source
        self.labels = labels
        self.created = created
        self.updated = updated

    @classmethod
    def from_dict(cls, obj: dict) -> "Metadata":
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
        return cls(**obj)
