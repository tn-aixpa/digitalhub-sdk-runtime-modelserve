"""
Client builder module.
"""
from sdk.client.client import Client


class ClientBuilder:
    """
    The client builder.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._instance = None

    def __call__(self):
        """
        Call method.
        """
        if not self._instance:
            self._instance = Client()
        return self._instance
