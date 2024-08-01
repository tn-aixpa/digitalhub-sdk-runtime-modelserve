from __future__ import annotations

from digitalhub_core.entities.run.spec import ENTITY_FUNC, RunParams, RunSpec
from digitalhub_data.entities.dataitem.crud import get_dataitem
from digitalhub_data.entities.entity_types import EntityTypes

ENTITY_FUNC[EntityTypes.DATAITEM.value] = get_dataitem


class RunSpecData(RunSpec):
    """Run specification."""


class RunParamsData(RunParams):
    """
    Run parameters.
    """
