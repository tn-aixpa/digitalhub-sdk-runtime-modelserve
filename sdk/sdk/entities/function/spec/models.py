"""
Function specification models module.
"""
from pydantic import BaseModel


class FunctionParams(BaseModel):
    """
    Function parameters model.
    """

    source: str
    """Path to the Function's source code on the local file system."""

    image: str
    """Name of the Function's container image."""

    tag: str
    """Tag of the Function's container image."""

    handler: str
    """Function handler name."""

    command: str
    """Command to run inside the container."""


class FunctionParamsJob(FunctionParams):
    """
    Function job parameters model.
    """

    requirements: list
    """List of requirements for the Function."""


class FunctionParamsDBT(FunctionParams):
    """
    Function DBT parameters model.
    """

    sql: str
    """SQL query to run inside the container."""
