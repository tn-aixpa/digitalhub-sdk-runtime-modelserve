"""
Client module.
"""
from typing import Union

import requests

from sdk.client.env_utils import get_dhub_env


class Client:
    def create_object(self, obj: dict, api: str):
        endpoint = self._get_endpoint(api)
        r = requests.post(endpoint, json=obj)
        d = self._dictify(r)
        self._parse_status(d)
        return d

    def get_object(self, api: str):
        endpoint = self._get_endpoint(api)
        r = requests.get(endpoint)
        d = self._dictify(r)
        self._parse_status(d)
        return d

    def update_object(self, obj: dict, api: str):
        endpoint = self._get_endpoint(api)
        r = requests.put(endpoint, json=obj)
        d = self._dictify(r)
        self._parse_status(d)
        return d

    def delete_object(self, api: str):
        endpoint = self._get_endpoint(api)
        r = requests.delete(endpoint)
        d = self._dictify(r)
        self._parse_status(d)
        return d

    @staticmethod
    def _parse_status(d: Union[dict, bool]) -> None:
        if isinstance(d, dict) and "status" in d:
            raise Exception(d)

    @staticmethod
    def _dictify(r: requests.Response) -> dict:
        try:
            return r.json()
        except Exception as ex:
            raise ex

    @staticmethod
    def _get_endpoint(api: str) -> str:
        endpoint = get_dhub_env().endpoint
        if endpoint is not None:
            return endpoint + api
        raise Exception(
            "Endpoint not setted. Please set env variables with 'set_dhub_env' function."
        )
