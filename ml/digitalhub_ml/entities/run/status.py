from __future__ import annotations

from digitalhub_data.entities.run.status import ENTITY_FUNC, RunStatusData
from digitalhub_ml.entities.model.crud import get_model

ENTITY_FUNC["models"] = get_model


class RunStatusMl(RunStatusData):
    """
    A class representing a run status.
    """
