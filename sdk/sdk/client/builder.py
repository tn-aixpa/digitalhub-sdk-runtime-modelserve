"""
Object factory module.
"""
from sdk.client.client import Client


class ClientBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self):
        if not self._instance:
            self._instance = Client()
        return self._instance
