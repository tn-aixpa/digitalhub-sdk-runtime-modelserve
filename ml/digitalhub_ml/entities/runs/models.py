from __future__ import annotations

from digitalhub_data.entities.runs.models import EntityInputsOutputsData


class EntityInputsOutputsMl(EntityInputsOutputsData):
    """
    Inputs/outputs model for runs.
    """

    models: list[str, dict]
    """List of model names, keys or objects."""
