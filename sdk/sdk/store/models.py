"""
Store models module.
"""
from typing import Literal

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class StoreConfig(BaseModel):
    """
    Store configuration class.
    """

    name: str
    """Store id."""

    type: Literal["s3", "local", "remote"]
    """Store type to instantiate."""

    uri: str
    """Store URI."""

    config: dict | None = None
    """Dictionary containing credentials/configurations for the storage."""

    is_default: bool = False
    """Flag to determine if the store is the default one."""
