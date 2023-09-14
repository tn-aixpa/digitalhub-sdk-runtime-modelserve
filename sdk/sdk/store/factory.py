"""
Store factory module.
"""
from sdk.store.builder import StoreBuilder
from sdk.store.models import StoreParameters
from sdk.store.objects.base import Store

store_builder = StoreBuilder()


def set_store(store_cfg: StoreParameters) -> None:
    """
    Set a new store instance with the given configuration.

    Parameters
    ----------
    store_cfg : StoreParameters
        Store configuration.

    Returns
    -------
    None
    """
    store_builder.build(store_cfg)


def get_store(uri: str) -> Store:
    """
    Get store instance by uri.

    Parameters
    ---------
    uri : str
        URI to parse.

    Returns
    -------
    Store
        Store instance.
    """
    return store_builder.get(uri)


def get_default_store() -> Store:
    """
    Get the default store instance. The default store is the one that
    can persist artifacts and dataitems.

    Returns
    -------
    Store
        Default store instance.
    """
    return store_builder.default()
