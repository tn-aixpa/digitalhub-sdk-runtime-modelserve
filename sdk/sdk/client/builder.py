"""
Client builder module.
"""
from __future__ import annotations

import os
import typing

from sdk.client.objects.dhcore import ClientDHCore
from sdk.client.objects.local import ClientLocal

if typing.TYPE_CHECKING:
    from sdk.client.objects.base import Client
    from sdk.client.objects.dhcore import DHCoreConfig


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


def set_dhub_env(config: DHCoreConfig) -> None:
    """
    Function to set environment variables for DHub Core config.

    Parameters
    ----------
    config : DHCoreConfig
        An object that contains endpoint, user, password, and token of a DHub Core configuration.

    Returns
    -------
    None
    """
    os.environ["DHUB_CORE_ENDPOINT"] = config.endpoint
    os.environ["DHUB_CORE_USER"] = config.user or ""
    os.environ["DHUB_CORE_PASSWORD"] = config.password or ""
    os.environ["DHUB_CORE_TOKEN"] = config.token or ""
