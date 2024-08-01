from __future__ import annotations

from digitalhub_data.entities.run.spec import ENTITY_FUNC, RunParamsData, RunSpecData
from digitalhub_ml.entities.entity_types import EntityTypes
from digitalhub_ml.entities.model.crud import get_model

ENTITY_FUNC[EntityTypes.MODEL.value] = get_model


class RunSpecMl(RunSpecData):
    """Run specification."""


class RunParamsMl(RunParamsData):
    """
    Run parameters.
    """
