from __future__ import annotations

from digitalhub_core.entities._base.spec import SpecRegistry
from digitalhub_core.entities._base.status import StatusRegistry

status_registry = StatusRegistry()
status_registry.register(
    "nefertem",
    "digitalhub_data_nefertem.entities.functions.status",
    "FunctionStatusNefertem",
)
status_registry.register(
    "nefertem+infer",
    "digitalhub_data_nefertem.entities.tasks.status",
    "TaskStatusInfer",
)
status_registry.register(
    "nefertem+metric",
    "digitalhub_data_nefertem.entities.tasks.status",
    "TaskStatusMetric",
)
status_registry.register(
    "nefertem+profile",
    "digitalhub_data_nefertem.entities.tasks.status",
    "TaskStatusProfile",
)
status_registry.register(
    "nefertem+validate",
    "digitalhub_data_nefertem.entities.tasks.status",
    "TaskStatusValidate",
)
status_registry.register(
    "nefertem+run",
    "digitalhub_data_nefertem.entities.runs.status",
    "RunStatusNefertem",
)

spec_registry = SpecRegistry()
spec_registry.register(
    "nefertem",
    "digitalhub_data_nefertem.entities.functions.spec",
    "FunctionSpecNefertem",
    "FunctionParamsNefertem",
)
spec_registry.register(
    "nefertem+infer",
    "digitalhub_data_nefertem.entities.tasks.spec",
    "TaskSpecInfer",
    "TaskParamsInfer",
)
spec_registry.register(
    "nefertem+metric",
    "digitalhub_data_nefertem.entities.tasks.spec",
    "TaskSpecMetric",
    "TaskParamsMetric",
)
spec_registry.register(
    "nefertem+profile",
    "digitalhub_data_nefertem.entities.tasks.spec",
    "TaskSpecProfile",
    "TaskParamsProfile",
)
spec_registry.register(
    "nefertem+validate",
    "digitalhub_data_nefertem.entities.tasks.spec",
    "TaskSpecValidate",
    "TaskParamsValidate",
)
spec_registry.register(
    "nefertem+run",
    "digitalhub_data_nefertem.entities.runs.spec",
    "RunSpecNefertem",
    "RunParamsNefertem",
)
