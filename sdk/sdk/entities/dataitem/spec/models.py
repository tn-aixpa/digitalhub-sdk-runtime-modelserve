"""
Dataitem specification models module.
"""
from pydantic import BaseModel


class DataitemParams(BaseModel):
    """
    Dataitem parameters.
    """

    key: str
    """The key of the dataitem."""
    path: str
    "The path of the dataitem."


class DataitemParamsTable(DataitemParams):
    """
    Dataitem table parameters.
    """


class DataitemParamsDBT(DataitemParams):
    """
    Dataitem DBT parameters.
    """

    raw_code: str
    "The raw code of the dataitem."

    compiled_code: str
    "The compiled code of the dataitem."
