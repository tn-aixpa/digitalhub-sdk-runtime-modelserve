from __future__ import annotations

from oltreai_data.entities.run.spec import ENTITY_FUNC, RunParamsData, RunSpecData
from oltreai_ml.entities.entity_types import EntityTypes
from oltreai_ml.entities.model.crud import get_model

ENTITY_FUNC[EntityTypes.MODEL.value] = get_model


class RunSpecMl(RunSpecData):
    """Run specification."""


class RunParamsMl(RunParamsData):
    """
    Run parameters.
    """
