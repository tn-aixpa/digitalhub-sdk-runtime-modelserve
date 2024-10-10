from __future__ import annotations

from pydantic import Field

from digitalhub.entities._base.spec.material import MaterialParams, MaterialSpec
from digitalhub.entities.dataitem.models import TableSchema


class DataitemSpec(MaterialSpec):
    """
    Dataitem specifications.
    """


class DataitemParams(MaterialParams):
    """
    Dataitem parameters.
    """


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

    def __init__(self, path: str, schema: dict | None = None) -> None:
        super().__init__(path)
        self.schema = schema


class DataitemParamsTable(DataitemParams):
    """
    Dataitem table parameters.
    """

    schema_: TableSchema = Field(default=None, alias="schema")
    """The schema of the dataitem in table schema format."""


class DataitemSpecIceberg(DataitemSpec):
    """
    Dataitem iceberg specifications.
    """


class DataitemParamsIceberg(DataitemParams):
    """
    Dataitem iceberg parameters.
    """
