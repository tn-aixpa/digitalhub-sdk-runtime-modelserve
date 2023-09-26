"""
Run specification models module.
"""

from pydantic import BaseModel


class Objects(BaseModel):
    """
    Run inputs specification.
    """

    dataitems: list[str] | None = None
    """List of dataitems names."""

    artifacts: list[str] | None = None
    """List of artifacts names."""


class RunParams(BaseModel):
    """
    Run parameters.
    """

    task: str | None = None
    """The task associated with the run."""

    inputs: Objects | None = {}
    """List of input dataitems and artifacts names."""

    outputs: Objects | None = {}
    """List of output dataitems and artifacts names."""

    parameters: dict | None = {}
    """Parameters to be used in the run."""

    local_execution: bool = False
    """Flag to indicate if the run will be executed locally."""
