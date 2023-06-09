"""
Stores registry module.
"""
from sdk.store.objects.local import LocalStore
from sdk.store.objects.s3 import S3Store
from sdk.store.objects.dummy import DummyStore

STORES = {
    "local": LocalStore,
    "s3": S3Store,
    "dummy": DummyStore,
}
