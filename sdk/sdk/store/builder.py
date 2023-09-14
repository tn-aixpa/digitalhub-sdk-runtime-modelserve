"""
Store builder module.
"""
from __future__ import annotations

import typing

from pydantic import ValidationError

from sdk.store.env_utils import get_env_store_config
from sdk.store.models import StoreParameters
from sdk.store.objects.local import LocalStore
from sdk.store.objects.remote import RemoteStore
from sdk.store.objects.s3 import S3Store
from sdk.store.objects.sql import SqlStore
from sdk.utils.exceptions import StoreError
from sdk.utils.uri_utils import map_uri_scheme

if typing.TYPE_CHECKING:
    from sdk.store.objects.base import Store


REGISTRY_STORES = {
    "local": LocalStore,
    "s3": S3Store,
    "remote": RemoteStore,
    "sql": SqlStore,
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

    def build(self, store_cfg: StoreParameters) -> None:
        """
        Build a store instance and register it.

        Parameters
        ----------
        store_cfg : StoreParameters
            Store configuration.

        Returns
        -------
        None
        """
        scheme = store_cfg.type
        if scheme not in self._instances:
            self._instances[scheme] = self.build_store(store_cfg)

    def get(self, uri: str) -> Store:
        """
        Get a store instance by URI.

        Parameters
        ----------
        uri : str
            URI to parse.

        Returns
        -------
        Store
            The store instance.
        """
        scheme = map_uri_scheme(uri)
        try:
            return self._instances[scheme]
        except KeyError:
            store_cfg = get_env_store_config(scheme)
            self.build_store(store_cfg)
            return self._instances[scheme]

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

    def build_store(self, cfg: StoreParameters) -> Store:
        """
        Build a store instance.

        Parameters
        ----------
        cfg : StoreParameters
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
            obj = REGISTRY_STORES[cfg.type](cfg.name, cfg.type, cfg.config)
            if cfg.is_default:
                if self._default is not None:
                    raise StoreError("Only one default store!")
                self._default = obj
            return obj
        except KeyError as exc:
            raise NotImplementedError from exc

    @staticmethod
    def _check_config(config: StoreParameters | dict) -> StoreParameters:
        """
        Check the store configuration validity.

        Parameters
        ----------
        config : StoreParameters | dict
            The store configuration.

        Returns
        -------
        StoreParameters
            The store configuration.

        Raises
        ------
        TypeError
            If the config parameter is not a StoreParameters instance or a well-formed dictionary.
        """
        if not isinstance(config, StoreParameters):
            try:
                return StoreParameters(**config)
            except TypeError as exc:
                raise StoreError("Invalid store configuration type.") from exc
            except ValidationError as exc:
                raise StoreError("Malformed store configuration parameters.") from exc
        return config
