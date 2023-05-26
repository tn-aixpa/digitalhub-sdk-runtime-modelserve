"""
Module for models.
"""
from typing import Literal, Optional

from pydantic import BaseModel


class DHCoreConfig(BaseModel):
    """
    DigitalHUB backend configuration.
    """

    endpoint: Optional[str] = None
    """Backend endpoint."""

    user: Optional[str] = None
    """User."""

    password: Optional[str] = None
    """Password."""

    token: Optional[str] = None
    """Auth token."""


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

    description: Optional[str] = None
    """Human readable name for Store."""

    isDefault: Optional[bool] = False
    """Determine if a Store is the default one."""

    config: Optional[dict] = None
    """Dictionary containing credentials/configurations for the storage."""
