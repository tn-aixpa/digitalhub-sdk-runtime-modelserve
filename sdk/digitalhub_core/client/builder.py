"""
Client builder module.
"""
from __future__ import annotations

import typing

from digitalhub_core.client.objects.dhcore import ClientDHCore
from digitalhub_core.client.objects.local import ClientLocal

if typing.TYPE_CHECKING:
    from digitalhub_core.client.objects.base import Client


class ClientBuilder:
    """
    The client builder. It implements the builder pattern to create a client instance.
    """

    def __init__(self) -> None:
        self._client = None

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
        if self._client is None:
            if local:
                self._client = ClientLocal()
            else:
                self._client = ClientDHCore()
        return self._client


def get_client(local: bool = False) -> Client:
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
