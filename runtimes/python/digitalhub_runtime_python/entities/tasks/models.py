from __future__ import annotations

from pydantic import BaseModel


class CorePort(BaseModel):
    """
    Port mapper model.
    """

    port: int
    target_port: int


class ContextRef(BaseModel):
    """
    ContextRef model.
    """

    destination: str = None
    protocol: str = None
    source: str = None


class ContextSource(BaseModel):
    """
    ContextSource model.
    """

    base64: str = None
    name: str = None
