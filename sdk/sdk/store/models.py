"""
Module for models.
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

    config: Optional[dict] = None
    """Dictionary containing credentials/configurations for the storage."""
