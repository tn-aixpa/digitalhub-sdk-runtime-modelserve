from __future__ import annotations

from digitalhub_core.entities._base.spec import SpecRegistry
from digitalhub_core.entities._base.status import StatusRegistry

status_registry = StatusRegistry()
status_registry.register(
    "nefertem_frictionless",
    "digitalhub_core.entities.functions.status",
    "FunctionStatus",
)
status_registry.register(
    "nefertem_frictionless+infer",
    "digitalhub_core.entities.tasks.status",
    "TaskStatus",
)
status_registry.register(
    "nefertem_frictionless+profile",
    "digitalhub_core.entities.tasks.status",
    "TaskStatus",
)
status_registry.register(
    "nefertem_frictionless+validate",
    "digitalhub_core.entities.tasks.status",
    "TaskStatus",
)
status_registry.register(
    "nefertem_frictionless+run",
    "digitalhub_data_nefertem_frictionless.entities.runs.status",
    "RunStatusNefertemFrictionless",
)

spec_registry = SpecRegistry()
spec_registry.register(
    "nefertem_frictionless",
    "digitalhub_data_nefertem_frictionless.entities.functions.spec",
    "FunctionSpecNefertemFrictionless",
    "FunctionParamsNefertemFrictionless",
)
spec_registry.register(
    "nefertem_frictionless+infer",
    "digitalhub_data_nefertem_frictionless.entities.tasks.spec",
    "TaskSpecInfer",
    "TaskParamsInfer",
)
spec_registry.register(
    "nefertem_frictionless+profile",
    "digitalhub_data_nefertem_frictionless.entities.tasks.spec",
    "TaskSpecProfile",
    "TaskParamsProfile",
)
spec_registry.register(
    "nefertem_frictionless+validate",
    "digitalhub_data_nefertem_frictionless.entities.tasks.spec",
    "TaskSpecValidate",
    "TaskParamsValidate",
)
spec_registry.register(
    "nefertem_frictionless+run",
    "digitalhub_data_nefertem_frictionless.entities.runs.spec",
    "RunSpecNefertemFrictionless",
    "RunParamsNefertemFrictionless",
)
