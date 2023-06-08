from __future__ import annotations

import typing
from typing import Union

from sdk.store.models import StoreConfig
from sdk.store.registry import STORES

if typing.TYPE_CHECKING:
    from sdk.store.objects.store import Store


class StoreBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, store_cfg: StoreConfig = None):
        if self._instance is None:
            if store_cfg is None:
                store_cfg = StoreConfig(name="dummy", type="dummy", config={})
            self._instance = self.build_store(store_cfg)
        return self._instance

    def build_store(self, cfg: StoreConfig) -> Store:
        """
        Method to create stores.
        """
        try:
            return STORES[cfg.type](cfg.name, cfg.type, cfg.config)
        except KeyError:
            raise NotImplementedError

    @staticmethod
    def _check_config(config: Union[StoreConfig, dict]) -> StoreConfig:
        """
        Try to convert a dictionary in a StoreConfig model.
        In case the config parameter is None, return a dummy store basic
        config.
        """
        if not isinstance(config, StoreConfig):
            try:
                return StoreConfig(**config)
            except TypeError:
                raise TypeError("Malformed store configuration.")
        return config
