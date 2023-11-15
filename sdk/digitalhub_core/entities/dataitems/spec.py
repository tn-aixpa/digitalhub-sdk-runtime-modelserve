"""
Dataitem specification module.
"""
from pydantic import BaseModel

from digitalhub_core.entities._base.spec import Spec


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

    key: str | None = None
    """The key of the dataitem."""
    path: str | None = None
    "The path of the dataitem."
