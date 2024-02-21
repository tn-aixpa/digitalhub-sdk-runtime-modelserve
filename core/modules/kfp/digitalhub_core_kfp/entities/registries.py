from __future__ import annotations

from digitalhub_core.entities._base.spec import SpecRegistry
from digitalhub_core.entities._base.status import StatusRegistry

status_registry = StatusRegistry()
status_registry.register("kfp", "digitalhub_core.entities.functions.status", "FunctionStatus")
status_registry.register("kfp+pipeline", "digitalhub_core.entities.tasks.status", "TaskStatus")
status_registry.register("kfp+run", "digitalhub_core_kfp.entities.runs.status", "RunStatusKFP")

spec_registry = SpecRegistry()
spec_registry.register(
    "kfp", "digitalhub_core_kfp.entities.functions.spec", "FunctionSpecKFP", "FunctionParamsKFP"
)
spec_registry.register("kfp+pipeline", "digitalhub_core_kfp.entities.tasks.spec", "TaskSpecPipeline", "TaskParamsPipeline")
spec_registry.register("kfp+run", "digitalhub_core_kfp.entities.runs.spec", "RunSpecKFP", "RunParamsKFP")