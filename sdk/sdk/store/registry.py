from sdk.store.objects.local import LocalStore
from sdk.store.objects.s3 import S3Store


SCHEME_LOCAL = ["", "file"]
SCHEME_S3 = ["s3"]


STORES = {
    "local": LocalStore,
    "s3": S3Store,
}
