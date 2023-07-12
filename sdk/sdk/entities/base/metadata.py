"""
Entity metadata module.
"""
from sdk.entities.base.base_model import ModelObj


class EntityMetadata(ModelObj):
    """
    A class representing the metadata of an entity.
    """

    def __init__(self, name: str = None, description: str = "") -> None:
        """
        Constructor.

        Parameters
        ----------
        name : str
            Name of the entity.
        description : str
            Description of the entity.
        """
        self.name = name
        self.description = description

    @classmethod
    def from_dict(cls, obj: dict = None) -> "EntityMetadata":
        """
        Return entity metadata object from dictionary.

        Parameters
        ----------
        obj : dict
            A dictionary containing the attributes of the entity metadata.

        Returns
        -------
        EntityMetadata
            An entity metadata object.

        """
        if obj is None:
            obj = {}
        return cls(**obj)
