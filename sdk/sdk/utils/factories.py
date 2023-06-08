"""
Object factory module.
"""
from __future__ import annotations
import typing
from typing import Any

from sdk.client.builder import ClientBuilder
from sdk.store.builder import StoreBuilder

if typing.TYPE_CHECKING:
    from sdk.store.models import StoreConfig


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


factory = ObjectFactory()
factory.register_builder("client", ClientBuilder())
factory.register_builder("store", StoreBuilder())


def get_client():
    return factory.create("client")


def set_store(store_cfg: StoreConfig):
    factory.create("store", store_cfg=store_cfg)


def get_store():
    return factory.create("store")
