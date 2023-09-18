"""
Environment utilities for the stores.
"""
import os

from sdk.store.models import (
    LocalStoreConfig,
    RemoteStoreConfig,
    S3StoreConfig,
    SQLStoreConfig,
    StoreParameters,
)


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
                endpoint_url=os.getenv("S3_ENDPOINT_URL"),
                aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"),
                bucket_name=os.getenv("S3_BUCKET_NAME"),
            ),
        )
    elif scheme == "sql":
        return StoreParameters(
            name="sql",
            type="sql",
            config=SQLStoreConfig(
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                database=os.getenv("POSTGRES_DATABASE"),
                pg_schema=os.getenv("POSTGRES_SCHEMA"),
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
