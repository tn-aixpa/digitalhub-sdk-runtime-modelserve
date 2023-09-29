"""
Entity specification module.
"""
from sdk.entities.base.base import ModelObj


class EntitySpec(ModelObj):
    """
    A class representing the specification of an entity.
    """

    @classmethod
    def from_dict(cls, obj: dict | None = None) -> "EntitySpec":
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
        obj = obj if obj is not None else {}
        return cls(**obj)
