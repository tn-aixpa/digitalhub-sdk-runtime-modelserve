"""
Run specification models module.
"""

from pydantic import BaseModel


class Objects(BaseModel):
    """
    Run inputs specification.
    """

    dataitems: list[str] | None = None
    artifacts: list[str] | None = None


class RunParams(BaseModel):
    """
    Run parameters.
    """

    inputs: Objects | None = None
    """List of input dataitems and artifacts names."""

    outputs: Objects | None = None
    """List of output dataitems and artifacts names."""

    parameters: dict | None = None
    """Parameters to be used in the run."""

    local_execution: bool = False
    """Flag to indicate if the run will be executed locally."""
