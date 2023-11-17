"""
Dataitem specification module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.spec import Spec
from pydantic import BaseModel


class DataitemSpec(Spec):
    """
    Dataitem specifications.
    """

    def __init__(self, key: str | None = None, path: str | None = None, **kwargs) -> None:
        """
        Constructor.

        Parameters
        ----------
        key : str
            The key of the dataitem.
        path : str
            The path of the dataitem.
        **kwargs
            Keyword arguments.
        """
        self.key = key
        self.path = path

        self._any_setter(**kwargs)


class DataitemParams(BaseModel):
    """
    Dataitem parameters.
    """

    key: str = None
    """The key of the dataitem."""
    path: str = None
    "The path of the dataitem."
