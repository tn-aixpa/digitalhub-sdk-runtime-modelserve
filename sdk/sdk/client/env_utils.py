"""
Environment variables utilities for DHub Core configuration.
"""
import os

from sdk.client.models import DHCoreConfig


def get_dhub_env() -> DHCoreConfig:
    """
    Function to get DHub Core environment variables.

    Returns
    -------
    DHCoreConfig
        An object that contains endpoint, user, password, and token of a DHub Core configuration.
    """
    return DHCoreConfig(
        endpoint=os.getenv("DHUB_CORE_ENDPOINT"),
        user=os.getenv("DHUB_CORE_USER"),
        password=os.getenv("DHUB_CORE_PASSWORD"),
        token=os.getenv("DHUB_CORE_TOKEN"),
    )


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
