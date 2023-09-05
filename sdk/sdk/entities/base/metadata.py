"""
Entity metadata module.
"""
from sdk.entities.base.base_model import ModelObj


class Metadata(ModelObj):
    """
    A class representing the metadata of an entity.
    """

    def __init__(
        self, name: str | None = None, description: str | None = None, **kwargs
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        name : str
            Name of the object.
        description : str
            Description of the entity.
        **kwargs
            Keyword arguments.
        """
        self.name = name
        self.description = description

        self._any_setter(**kwargs)

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
        if obj is None:
            obj = {}
        return cls(**obj)


def build_metadata(
    name: str | None = None, description: str | None = None, **kwargs
) -> Metadata:
    """
    Build entity metadata object.

    Parameters
    ----------
    name : str
        Name of the object.
    description : str
        Description of the entity.

    Returns
    -------
    Metadata
        An entity metadata object.
    """
    return Metadata(name=name, description=description, **kwargs)
