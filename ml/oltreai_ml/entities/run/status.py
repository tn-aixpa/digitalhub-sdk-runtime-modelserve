from __future__ import annotations

from oltreai_data.entities.run.status import ENTITY_FUNC, RunStatusData
from oltreai_ml.entities.entity_types import EntityTypes
from oltreai_ml.entities.model.crud import get_model

ENTITY_FUNC[EntityTypes.MODEL.value] = get_model


class RunStatusMl(RunStatusData):
    """
    A class representing a run status.
    """
