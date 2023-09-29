"""
Project specification models module.
"""
from pydantic import BaseModel


class ProjectParams(BaseModel):
    context: str
    """The project's context."""

    source: str
    """The project's source."""

    functions: list
    """List of project's functions."""

    artifacts: list
    """List of project's artifacts."""

    workflows: list
    """List of project's workflows."""

    dataitems: list
    """List of project's dataitems."""
