"""
Store builder module.
"""
from __future__ import annotations

import typing
from typing import Union

from sdk.store.models import StoreConfig
from sdk.store.registry import STORES

if typing.TYPE_CHECKING:
    from sdk.store.objects.store import Store


class StoreBuilder:
    """
    Store builder class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self._instances = {}
        self._default = None

    def build(self, store_cfg: StoreConfig) -> None:
        """
        Build a store instance and register it.

        Parameters
        ----------
        store_cfg : StoreConfig
            Store configuration.

        Returns
        -------
        None
        """
        if store_cfg.name not in self._instances:
            self._instances[store_cfg.name] = self.build_store(store_cfg)

    def get(self, store_name: str) -> Store:
        """
        Get a store instance.

        Parameters
        ----------
        store_name : str
            Store name.

        Returns
        -------
        Store
            The store instance.
        """
        return self._instances[store_name]

    def default(self) -> Store:
        """
        Get the default store instance.

        Returns
        -------
        Store
            The default store instance.

        Raises
        ------
        Exception
            If no default store is setted.
        """
        if self._default is None:
            raise Exception("No default store setted.")
        return self._default

    def build_store(self, cfg: StoreConfig) -> Store:
        """
        Build a store instance.

        Parameters
        ----------
        cfg : StoreConfig
            Store configuration.

        Returns
        -------
        Store
            The store instance.

        Raises
        ------
        NotImplementedError
            If the store type is not implemented.
        """
        try:
            obj = STORES[cfg.type](cfg.name, cfg.type, cfg.uri, cfg.config)
            if cfg.is_default:
                if self._default is not None:
                    raise Exception("Only one default store!")
                self._default = obj
            return obj
        except KeyError as exc:
            raise NotImplementedError from exc

    @staticmethod
    def _check_config(config: Union[StoreConfig, dict]) -> StoreConfig:
        """
        Check the store configuration validity.

        Parameters
        ----------
        config : Union[StoreConfig, dict]
            The store configuration.

        Returns
        -------
        StoreConfig
            The store configuration.

        Raises
        ------
        TypeError
            If the config parameter is not a StoreConfig instance or a well formed dictionary.
        """
        if not isinstance(config, StoreConfig):
            try:
                return StoreConfig(**config)
            except TypeError as exc:
                raise TypeError("Malformed store configuration.") from exc
        return config
