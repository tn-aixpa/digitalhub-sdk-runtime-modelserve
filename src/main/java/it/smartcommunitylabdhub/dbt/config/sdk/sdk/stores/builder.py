"""
Store builder module.
"""
from __future__ import annotations

import typing

from pydantic import ValidationError

from sdk.stores.env_utils import get_env_store_config
from sdk.stores.models import StoreParameters
from sdk.stores.registry import REGISTRY_STORES
from sdk.utils.exceptions import StoreError
from sdk.utils.uri_utils import map_uri_scheme

if typing.TYPE_CHECKING:
    from sdk.stores.objects.base import Store


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
        It overrides any existing instance.

        Parameters
        ----------
        store_cfg : StoreParameters
            Store configuration.

        Returns
        -------
        None
        """
        scheme = map_uri_scheme(store_cfg.type)
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
        if scheme not in self._instances:
            store_cfg = get_env_store_config(scheme)
            self._instances[scheme] = self.build_store(store_cfg)
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

    def set_default(self, scheme: str) -> None:
        """
        Set the default store instance.

        Parameters
        ----------
        scheme : str
            Store scheme.

        Returns
        -------
        None
        """
        self._default = self.get(scheme)

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
            if cfg.is_default and self._default is not None:
                raise StoreError("Only one default store!")
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


def set_store(store_cfg: StoreParameters) -> None:
    """
    Set a new store instance with the given configuration.

    Parameters
    ----------
    store_cfg : StoreParameters
        Store configuration.

    Returns
    -------
    None
    """
    store_builder.build(store_cfg)


def get_store(uri: str) -> Store:
    """
    Get store instance by uri.

    Parameters
    ---------
    uri : str
        URI to parse.

    Returns
    -------
    Store
        Store instance.
    """
    return store_builder.get(uri)


def get_default_store() -> Store:
    """
    Get the default store instance. The default store is the one that
    can persist artifacts and dataitems.

    Returns
    -------
    Store
        Default store instance.
    """
    return store_builder.default()


def set_default_store(scheme: str) -> None:
    """
    Set the default store instance.

    Parameters
    ----------
    scheme : str
        URI scheme.

    Returns
    -------
    None
    """
    store_builder.set_default(scheme)


store_builder = StoreBuilder()
