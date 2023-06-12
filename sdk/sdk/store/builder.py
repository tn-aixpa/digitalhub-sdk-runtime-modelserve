"""
Store builder module.
"""
from __future__ import annotations

import typing
from typing import Literal, Union

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

    def __call__(
        self,
        options: Literal["add", "get", "default"],
        store_cfg: StoreConfig = None,
        store_name: str = None,
    ) -> Store:
        """
        Call method.
        """
        if options == "add":
            if store_cfg.name not in self._instances:
                self._instances[store_cfg.name] = self.build_store(store_cfg)
            return

        if options == "get":
            return self._instances[store_name]

        if options == "default":
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
                else:
                    self._default = obj
            return obj
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
