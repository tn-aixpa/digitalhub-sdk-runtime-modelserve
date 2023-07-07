"""
Entity specification module.
"""
from sdk.entities.base.base_model import ModelObj


class EntitySpec(ModelObj):
    """
    A class representing the specification of an entity.
    """

    @classmethod
    def from_dict(cls, obj: dict = None) -> "EntitySpec":
        """
        Return entity specification object from dictionary.

        Parameters
        ----------
        obj : dict
            A dictionary containing the attributes of the entity specification.

        Returns
        -------
        EntitySpec
            An entity specification object.

        """
        if obj is None:
            obj = {}
        return cls(**obj)
