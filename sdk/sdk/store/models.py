"""
Store models module.
"""
from typing import Literal, Optional

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

    config: Optional[dict] = None
    """Dictionary containing credentials/configurations for the storage."""

    is_default: Optional[bool] = False
    """Flag to determine if the store is the default one."""
