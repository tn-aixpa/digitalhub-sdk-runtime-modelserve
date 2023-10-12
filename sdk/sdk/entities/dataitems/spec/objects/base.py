"""
Dataitem specification module.
"""
from pydantic import BaseModel

from sdk.entities.base.spec import EntitySpec


class DataitemSpec(EntitySpec):
    """
    Dataitem specifications.
    """

    def __init__(
        self, key: str | None = None, path: str | None = None, **kwargs
    ) -> None:
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

    key: str
    """The key of the dataitem."""
    path: str
    "The path of the dataitem."
