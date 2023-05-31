"""
Object factory module.
"""
from typing import Any

from sdk.models.models import DHCoreConfig, StoreConfig
from sdk.client.client import Client


class ObjectFactory:
    def __init__(self):
        self._builders = {}

    def register_builder(self, key: str, builder: Any):
        self._builders[key] = builder

    def create(self, key: str, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)


class ClientBuilder:
    def __init__(self):
        self._instance = None

    def __call__(
        self, dhub_cfg: "DHCoreConfig" = None, store_cfg: "StoreConfig" = None
    ):
        if not self._instance:
            self._instance = Client(dhub_cfg, store_cfg)
        return self._instance


factory = ObjectFactory()
factory.register_builder("client", ClientBuilder())
