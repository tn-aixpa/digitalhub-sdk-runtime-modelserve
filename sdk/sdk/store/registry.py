"""
Registry of store types.
"""
from sdk.store.objects.local import LocalStore
from sdk.store.objects.remote import RemoteStore
from sdk.store.objects.s3 import S3Store
from sdk.store.objects.sql import SqlStore

REGISTRY_STORES = {
    "local": LocalStore,
    "s3": S3Store,
    "remote": RemoteStore,
    "sql": SqlStore,
}
