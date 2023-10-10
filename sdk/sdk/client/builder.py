"""
Client builder module.
"""
from __future__ import annotations

import typing

from sdk.client.objects.dhcore import ClientDHCore
from sdk.client.objects.local import ClientLocal

if typing.TYPE_CHECKING:
    from sdk.client.objects.base import Client


class ClientBuilder:
    """
    The client builder. It implements the builder pattern to create a client instance.
    """

    def __init__(self) -> None:
        self._local_client: ClientLocal = None
        self._dhcore_client: ClientDHCore = None

    def build(self, local: bool = False) -> Client:
        """
        Method to create a client instance.

        Parameters
        ----------
        local : bool
            Whether to create a local client or not.

        Returns
        -------
        Client
            Returns the client instance.
        """
        if local:
            if self._local_client is None:
                self._local_client = ClientLocal()
            return self._local_client
        if self._dhcore_client is None:
            self._dhcore_client = ClientDHCore()
        return self._dhcore_client


def get_client(local: bool = False) -> ClientDHCore:
    """
    Wrapper around ClientBuilder.build.

    Parameters
    ----------
    local : bool
        Whether to create a local client or not.

    Returns
    -------
    Client
        The client instance.
    """
    return client_builder.build(local)


client_builder = ClientBuilder()
