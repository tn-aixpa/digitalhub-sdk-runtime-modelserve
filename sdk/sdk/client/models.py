"""
Module for models.
"""
from pydantic import BaseModel


class DHCoreConfig(BaseModel):
    """
    DigitalHUB backend configuration.
    """

    endpoint: str
    """Backend endpoint."""

    user: str | None = None
    """User."""

    password: str | None = None
    """Password."""

    token: str | None = None
    """Auth token."""
