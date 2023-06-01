"""
Object factory module.
"""
from typing import Any

from sdk.models.models import DHCoreConfig, StoreConfig
from sdk.client.client import Client
from sdk.client.utils import get_dhub_env, get_store_env


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


def get_client():
    dh_cfg = get_dhub_env()
    store_cfg = get_store_env()
    return factory.create("client", dhub_cfg=dh_cfg, store_cfg=store_cfg)
