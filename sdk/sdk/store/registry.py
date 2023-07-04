"""
Stores registry module.
"""
from sdk.store.objects.local import LocalStore
from sdk.store.objects.remote import RemoteStore
from sdk.store.objects.s3 import S3Store

STORES = {
    "local": LocalStore,
    "s3": S3Store,
    "remote": RemoteStore,
}
