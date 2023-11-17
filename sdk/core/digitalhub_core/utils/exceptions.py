"""
Exceptions module.
"""
from __future__ import annotations


class GenericError(Exception):
    """
    Base class for exception.
    """


class StoreError(GenericError):
    """
    Raised when incontered errors on Stores.
    """


class BackendError(GenericError):
    """
    Raised when incontered errors from backend.
    """


class EntityError(GenericError):
    """
    Raised when incontered errors on Entities.
    """
