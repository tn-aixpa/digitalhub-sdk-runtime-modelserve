from __future__ import annotations

import typing
from pathlib import Path
from typing import Union

from sdk.store.models import StoreConfig
from sdk.store.registry import SCHEME_LOCAL, SCHEME_S3, STORES
from sdk.utils.file_utils import get_absolute_path
from sdk.utils.uri_utils import (
    get_uri_netloc,
    get_uri_path,
    get_uri_scheme,
    rebuild_uri,
)
from sdk.utils.utils import get_uiid

if typing.TYPE_CHECKING:
    from sdk.store.objects.store import Store


class StoreBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, store_cfg: StoreConfig = None):
        if self._instance is None:
            if store_cfg is None:
                raise Exception("Please set a store configuration.")
            self._instance = self.build_artifact_store(store_cfg)
        return self._instance

    def build_artifact_store(self, cfg: StoreConfig) -> Store:
        """
        Method to create a artifact stores.
        """
        scheme = get_uri_scheme(cfg.uri)
        new_uri = self.resolve_artifact_uri(cfg.uri, scheme)
        tmp = str(Path(cfg.tmp, get_uiid()))
        try:
            return STORES[cfg.type](cfg.name, cfg.type, new_uri, tmp, cfg.config)
        except KeyError:
            raise NotImplementedError

    @staticmethod
    def resolve_artifact_uri(uri: str, scheme: str) -> str:
        """
        Resolve artifact URI location.
        """
        if scheme in [*SCHEME_LOCAL]:
            return get_absolute_path(get_uri_netloc(uri), get_uri_path(uri), "artifact")
        if scheme in [*SCHEME_S3]:
            return rebuild_uri(uri, "artifact")
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
