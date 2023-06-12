"""
Store models module.
"""
from typing import Literal, Optional

from pydantic import BaseModel


class StoreConfig(BaseModel):
    """
    Store configuration class.
    """

    name: str
    """Store id."""

    type: Literal["s3", "local"]
    """Store type to instantiate."""

    uri: str
    """Store URI."""

    config: Optional[dict] = None
    """Dictionary containing credentials/configurations for the storage."""

    is_default: Optional[bool] = False
    """Flag to determine if the store is the default one."""
