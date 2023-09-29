"""
Registry of store types.
"""
from sdk.stores.objects.local import LocalStore
from sdk.stores.objects.remote import RemoteStore
from sdk.stores.objects.s3 import S3Store
from sdk.stores.objects.sql import SqlStore

REGISTRY_STORES = {
    "local": LocalStore,
    "s3": S3Store,
    "remote": RemoteStore,
    "sql": SqlStore,
}
