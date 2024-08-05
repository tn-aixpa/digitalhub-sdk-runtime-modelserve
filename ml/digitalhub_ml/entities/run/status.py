from __future__ import annotations

from digitalhub_data.entities.run.status import ENTITY_FUNC, RunStatusData
from digitalhub_ml.entities.entity_types import EntityTypes
from digitalhub_ml.entities.model.crud import get_model

ENTITY_FUNC[EntityTypes.MODEL.value] = get_model


class RunStatusMl(RunStatusData):
    """
    A class representing a run status.
    """
