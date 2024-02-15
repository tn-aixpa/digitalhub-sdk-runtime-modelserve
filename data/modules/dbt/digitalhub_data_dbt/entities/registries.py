from __future__ import annotations

from digitalhub_core.entities._base.spec import SpecRegistry
from digitalhub_core.entities._base.status import StatusRegistry

status_registry = StatusRegistry()
status_registry.register("dbt", "digitalhub_core.entities.functions.status", "FunctionStatus")
status_registry.register("dbt+transform", "digitalhub_core.entities.tasks.status", "TaskStatus")
status_registry.register("dbt+run", "digitalhub_data_dbt.entities.runs.status", "RunStatusDbt")

spec_registry = SpecRegistry()
spec_registry.register("dbt", "digitalhub_data_dbt.entities.functions.spec", "FunctionSpecDbt", "FunctionParamsDbt")
spec_registry.register(
    "dbt+transform", "digitalhub_data_dbt.entities.tasks.spec", "TaskSpecTransform", "TaskParamsTransform"
)
spec_registry.register("dbt+run", "digitalhub_data_dbt.entities.runs.spec", "RunSpecDbt", "RunParamsDbt")
