"""
Object factory module.
"""
from typing import Any

from sdk.client.builder import ClientBuilder
from sdk.store.builder import StoreBuilder
from sdk.entities.project.context import ContextBuilder


class ObjectFactory:
    """
    Object factory class.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._builders = {}

    def register_builder(self, key: str, builder: Any) -> None:
        """
        Register a builder.

        Parameters
        ----------
        key : str
            Key to register the builder.
        builder : Any
            The builder class.

        Returns
        -------
        None
        """
        self._builders[key] = builder

    def create(self, key: str, **kwargs) -> Any:
        """
        Create an object.

        Parameters
        ----------
        key : str
            Key to create the object.
        **kwargs
            The object parameters.

        Returns
        -------
        Any
            The created object.

        Raises
        ------
        ValueError
            If the key is not registered.
        """
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)


factory = ObjectFactory()
factory.register_builder("client", ClientBuilder())
factory.register_builder("store", StoreBuilder())
factory.register_builder("context", ContextBuilder())
