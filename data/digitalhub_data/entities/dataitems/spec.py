"""
Dataitem specification module.
"""
from __future__ import annotations

from digitalhub_core.entities._base.spec import Spec, SpecParams
from pydantic import Field


class DataitemSpec(Spec):
    """
    Dataitem specifications.
    """

    def __init__(self, path: str, schema: dict | None = None, **kwargs) -> None:
        """
        Constructor.

        Parameters
        ----------
        path : str
            The path of the dataitem.
        **kwargs
            Keyword arguments.
        """
        self.path = path
        self.schema = schema

        self._any_setter(**kwargs)


class DataitemParams(SpecParams):
    """
    Dataitem parameters.
    """

    path: str
    "The path of the dataitem."

    _schema: dict = Field(alias="schema")
    """The schema of the dataitem in table schema format."""


class DataitemSpecDataitem(DataitemSpec):
    """
    Dataitem dataitem specifications.
    """


class DataitemParamsDataitem(DataitemParams):
    """
    Dataitem dataitem parameters.
    """


class DataitemSpecTable(DataitemSpec):
    """
    Dataitem table specifications.
    """


class DataitemParamsTable(DataitemParams):
    """
    Dataitem table parameters.
    """


class DataitemSpecIceberg(DataitemSpec):
    """
    Dataitem iceberg specifications.
    """


class DataitemParamsIceberg(DataitemParams):
    """
    Dataitem iceberg parameters.
    """
