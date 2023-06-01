import os
from sdk.models.models import DHCoreConfig, StoreConfig


def set_dhub_env(dhub_cfg: DHCoreConfig) -> None:
    """
    Function to set environment variables for DHub Core config.

    Parameters
    ----------
    dhub_cfg : DHCoreConfig
        An object that contains endpoint, user, password, and token of a DHub Core configuration.

    Returns
    -------
    None
        This function does not return anything but sets environment variables.
    """
    os.environ["DHUB_CORE_ENDPOINT"] = dhub_cfg.endpoint
    os.environ["DHUB_CORE_USER"] = dhub_cfg.user
    os.environ["DHUB_CORE_PASSWORD"] = dhub_cfg.password
    os.environ["DHUB_CORE_TOKEN"] = dhub_cfg.token


def get_dhub_env() -> DHCoreConfig:
    """
    Function to get DHub Core environment variables.

    Returns
    -------
    DHCoreConfig
        An object that contains endpoint, user, password, and token of a DHub Core configuration.
    """
    return DHCoreConfig(
        endpoint=os.getenv("DHUB_CORE_ENDPOINT", "http://127.0.0.1:8080"),
        user=os.getenv("DHUB_CORE_USER", ""),
        password=os.getenv("DHUB_CORE_PASSWORD", ""),
        token=os.getenv("DHUB_CORE_TOKEN", ""),
    )


def set_store_env(store_cfg: StoreConfig) -> None:
    """
    Function to set environment variables for Store config.

    Parameters
    ----------
    store_cfg : StoreConfig
        An object that contains endpoint, user, password, and token of a Store configuration.

    Returns
    -------
    None
        This function does not return anything but sets environment variables.
    """
    ...


def get_store_env() -> StoreConfig:
    """
    Function to get Store environment variables.

    Returns
    -------
    StoreConfig
        An object that contains endpoint, user, password, and token of a Store configuration.
    """
    ...
