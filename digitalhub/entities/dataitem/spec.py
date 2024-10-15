from __future__ import annotations

from pydantic import Field

from digitalhub.entities._base.spec.material import MaterialSpec, MaterialValidator
from digitalhub.entities.dataitem.models import TableSchema


class DataitemSpec(MaterialSpec):
    """
    Dataitem specifications.
    """


class DataitemValidator(MaterialValidator):
    """
    Dataitem parameters.
    """


class DataitemSpecDataitem(DataitemSpec):
    """
    Dataitem dataitem specifications.
    """


class DataitemValidatorDataitem(DataitemValidator):
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


class DataitemValidatorTable(DataitemValidator):
    """
    Dataitem table parameters.
    """

    schema_: TableSchema = Field(default=None, alias="schema")
    """The schema of the dataitem in table schema format."""


class DataitemSpecIceberg(DataitemSpec):
    """
    Dataitem iceberg specifications.
    """


class DataitemValidatorIceberg(DataitemValidator):
    """
    Dataitem iceberg parameters.
    """
