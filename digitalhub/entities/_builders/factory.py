from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.entity import Entity


class EntityFactory:
    """
    Factory class for building entities.
    """

    def __init__(self):
        self._builders = {}

    def add_builder(self, name: str, builder):
        self._builders[name] = builder

    def build(self, entity_type: str, **kwargs) -> Entity:
        """
        Build entity object. The builder takes as input
        the type of entity's object to build and the keyword
        arguments to pass to the various entity's constructor.
        The specific Entity class is searched in the global
        registry, where lies info about where to find the class.
        The arguments are parsed, eventually adding default values,
        and then passed to the constructor.

        Parameters
        ----------
        entity_type : str
            Registry entry kind.
        **kwargs : dict
            Keyword arguments for the constructor.

        Returns
        -------
        Entity
            Entity object.
        """
        if entity_type not in self._builders:
            raise ValueError(f"Entity type {entity_type} not found")
        return self._builders[entity_type](**kwargs)
