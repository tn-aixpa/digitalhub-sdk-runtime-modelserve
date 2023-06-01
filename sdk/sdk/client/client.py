"""
Client module.
"""
import requests

from sdk.models.models import DHCoreConfig, StoreConfig
from sdk.client.utils import get_dhub_env, get_store_env


class Client:
    def __init__(
        self, dhub_cfg: "DHCoreConfig" = None, store_cfg: "StoreConfig" = None
    ) -> None:
        self.dhub_cfg = None
        self.store_cfg = None
        self._setup(dhub_cfg, store_cfg)

    def _setup(self, dhub_cfg: "DHCoreConfig" = None, store_cfg: "StoreConfig" = None):
        self.dhub_cfg = dhub_cfg if dhub_cfg is not None else get_dhub_env()
        self.store_cfg = store_cfg if store_cfg is not None else get_store_env()

    def create_object(self, obj: dict, api: str):
        endpoint = self._get_endpoint(api)
        r = requests.post(endpoint, json=obj)
        return self._parse_response(r)

    def get_object(self, api: str):
        endpoint = self._get_endpoint(api)
        r = requests.get(endpoint)
        return self._parse_response(r)

    def delete_object(self, api: str):
        endpoint = self._get_endpoint(api)
        r = requests.delete(endpoint)
        return self._parse_response(r)

    @staticmethod
    def _parse_response(r: requests.Response):
        return r.json()

    def _get_endpoint(self, api: str) -> str:
        return self.dhub_cfg.endpoint + api
