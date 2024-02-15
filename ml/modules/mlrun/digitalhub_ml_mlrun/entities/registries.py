from __future__ import annotations

from digitalhub_core.entities._base.spec import SpecRegistry
from digitalhub_core.entities._base.status import StatusRegistry

status_registry = StatusRegistry()
status_registry.register("mlrun", "digitalhub_core.entities.functions.status", "FunctionStatus")
status_registry.register("mlrun+job", "digitalhub_core.entities.tasks.status", "TaskStatus")
status_registry.register("mlrun+run", "digitalhub_ml_mlrun.entities.runs.status", "RunStatusMlrun")

spec_registry = SpecRegistry()
spec_registry.register(
    "mlrun", "digitalhub_ml_mlrun.entities.functions.spec", "FunctionSpecMlrun", "FunctionParamsMlrun"
)
spec_registry.register("mlrun+job", "digitalhub_ml_mlrun.entities.tasks.spec", "TaskSpecJob", "TaskParamsJob")
spec_registry.register("mlrun+run", "digitalhub_ml_mlrun.entities.runs.spec", "RunSpecMlrun", "RunParamsMlrun")
