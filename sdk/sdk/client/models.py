"""
Module for models.
"""
from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class DHCoreConfig(BaseModel):
    """
    DigitalHUB backend configuration.
    """

    endpoint: str
    """Backend endpoint."""

    user: Optional[str] = None
    """User."""

    password: Optional[str] = None
    """Password."""

    token: Optional[str] = None
    """Auth token."""
