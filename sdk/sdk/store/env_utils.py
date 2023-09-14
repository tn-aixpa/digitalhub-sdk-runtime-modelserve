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
                endpoint_url=os.getenv("S3_ENDPOINT_URL", "http://192.168.49.2:30080"),
                aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID", "minio"),
                aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY", "minio123"),
                bucket_name=os.getenv("S3_BUCKET_NAME", "mlrun"),
            ),
        )
    elif scheme == "sql":
        return StoreParameters(
            name="sql",
            type="sql",
            config=SQLStoreConfig(
                host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
                port=os.getenv("POSTGRES_PORT", "5433"),
                user=os.getenv("POSTGRES_USER", "testuser"),
                password=os.getenv("POSTGRES_PASSWORD", "testpassword"),
                database=os.getenv("POSTGRES_DATABASE", "dbt"),
                pg_schema=os.getenv("POSTGRES_SCHEMA", "public"),
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
                path="sdk",
            ),
        )
