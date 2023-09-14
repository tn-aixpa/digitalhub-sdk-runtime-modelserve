"""
Client factory module.
"""
from sdk.client.builder import ClientBuilder
from sdk.client.client import Client

client_builder = ClientBuilder()


def get_client() -> Client:
    """
    Get the client instance.

    Returns
    -------
    Client
        The client instance.
    """
    return client_builder.build()
