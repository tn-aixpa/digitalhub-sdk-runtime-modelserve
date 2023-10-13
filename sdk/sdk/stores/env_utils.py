"""
Environment utilities for the stores.
"""
import os

from sdk.stores.objects.base import StoreParameters
from sdk.stores.objects.local import LocalStoreConfig
from sdk.stores.objects.remote import RemoteStoreConfig
from sdk.stores.objects.s3 import S3StoreConfig
from sdk.stores.objects.sql import SQLStoreConfig


def get_env_store_config(scheme: str) -> StoreParameters:
    """
    Get a store configuration from the environment.

    Parameters
    ----------
    scheme : str
        URI scheme.

    Returns
    -------
    StoreParameters
        The store configuration based on the scheme.
    """
    if scheme == "s3":
        return StoreParameters(
            name="s3",
            type="s3",
            config=S3StoreConfig(
                endpoint_url=os.getenv("S3_ENDPOINT_URL"),  # type: ignore
                aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"),  # type: ignore
                aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"),  # type: ignore
                bucket_name=os.getenv("S3_BUCKET_NAME"),  # type: ignore
            ),
        )
    elif scheme == "sql":
        return StoreParameters(
            name="sql",
            type="sql",
            config=SQLStoreConfig(
                host=os.getenv("POSTGRES_HOST"),  # type: ignore
                port=os.getenv("POSTGRES_PORT"),  # type: ignore
                user=os.getenv("POSTGRES_USER"),  # type: ignore
                password=os.getenv("POSTGRES_PASSWORD"),  # type: ignore
                database=os.getenv("POSTGRES_DATABASE"),  # type: ignore
                pg_schema=os.getenv("POSTGRES_SCHEMA"),  # type: ignore
            ),
        )
    elif scheme == "remote":
        return StoreParameters(
            name="remote",
            type="remote",
            config=RemoteStoreConfig(),
        )
    elif scheme == "local":
        return StoreParameters(
            name="local",
            type="local",
            config=LocalStoreConfig(
                path="tempsdk",
            ),
        )
