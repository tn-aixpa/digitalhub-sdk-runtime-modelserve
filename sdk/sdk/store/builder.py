"""
Store builder module.
"""
from __future__ import annotations

import typing

from pydantic import ValidationError

from sdk.store.models import StoreConfig
from sdk.store.objects.local import LocalStore
from sdk.store.objects.remote import RemoteStore
from sdk.store.objects.s3 import S3Store
from sdk.utils.exceptions import StoreError

if typing.TYPE_CHECKING:
    from sdk.store.objects.base import Store


STORES = {
    "local": LocalStore,
    "s3": S3Store,
    "remote": RemoteStore,
}


class StoreBuilder:
    """
    Store builder class.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self._instances: dict[str, Store] = {}
        self._default: Store | None = None

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
        StoreError
            If no default store is set.
        """
        if self._default is None:
            raise StoreError("No default store set.")
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
                    raise StoreError("Only one default store!")
                self._default = obj
            return obj
        except KeyError as exc:
            raise NotImplementedError from exc

    @staticmethod
    def _check_config(config: StoreConfig | dict) -> StoreConfig:
        """
        Check the store configuration validity.

        Parameters
        ----------
        config : StoreConfig | dict
            The store configuration.

        Returns
        -------
        StoreConfig
            The store configuration.

        Raises
        ------
        TypeError
            If the config parameter is not a StoreConfig instance or a well-formed dictionary.
        """
        if not isinstance(config, StoreConfig):
            try:
                return StoreConfig(**config)
            except TypeError as exc:
                raise StoreError("Invalid store configuration type.") from exc
            except ValidationError as exc:
                raise StoreError("Malformed store configuration parameters.") from exc
        return config
