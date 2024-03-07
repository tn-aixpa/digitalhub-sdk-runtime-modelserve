from __future__ import annotations

from pydantic import BaseModel


class EntityInputsOutputs(BaseModel):
    """
    Inputs/outputs model for runs.
    """

    artifacts: list[str, dict] = None
    """List of artifact names, keys or objects."""
