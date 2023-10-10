"""
Store models module.
"""
from typing import Literal

from pydantic import BaseModel


class StoreConfig(BaseModel):
    """
    Store configuration base class.
    """


class S3StoreConfig(StoreConfig):
    """
    S3 store configuration class.
    """

    endpoint_url: str
    """S3 endpoint URL."""

    aws_access_key_id: str
    """AWS access key ID."""

    aws_secret_access_key: str
    """AWS secret access key."""

    bucket_name: str
    """S3 bucket name."""


class SQLStoreConfig(StoreConfig):
    """
    SQL store configuration class.
    """

    host: str
    """SQL host."""

    port: int
    """SQL port."""

    user: str
    """SQL user."""

    password: str
    """SQL password."""

    database: str
    """SQL database name."""

    pg_schema: str
    """SQL schema name."""


class RemoteStoreConfig(StoreConfig):
    """
    Remote store configuration class.
    """


class LocalStoreConfig(StoreConfig):
    """
    Local store configuration class.
    """

    path: str
    """Local path."""


class StoreParameters(BaseModel):
    """
    Store configuration class.
    """

    name: str
    """Store id."""

    type: Literal["local", "s3", "remote", "sql"]
    """Store type to instantiate."""

    config: StoreConfig | None = None
    """Configuration for the store."""

    is_default: bool = False
    """Flag to determine if the store is the default one."""
