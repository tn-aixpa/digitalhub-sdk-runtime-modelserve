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
        self._instance = None

    def __call__(self, store_cfg: StoreConfig = None) -> Store:
        """
        Call method.
        """
        if self._instance is None:
            if store_cfg is None:
                store_cfg = StoreConfig(name="dummy", type="dummy", config={})
            self._instance = self.build_store(store_cfg)
        return self._instance

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
            return STORES[cfg.type](cfg.name, cfg.type, cfg.config)
        except KeyError:
            raise NotImplementedError

    @staticmethod
    def _check_config(config: Union[StoreConfig, dict]) -> StoreConfig:
        """
        Try to convert a dictionary in a StoreConfig model. In case the config parameter is None, return a dummy store basic
        config.

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
            except TypeError:
                raise TypeError("Malformed store configuration.")
        return config
