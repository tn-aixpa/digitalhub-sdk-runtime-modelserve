from __future__ import annotations

from digitalhub_core.entities._base.spec import SpecRegistry
from digitalhub_core.entities._base.status import StatusRegistry

status_registry = StatusRegistry()
status_registry.register(
    "container",
    "digitalhub_core_container.entities.functions.status",
    "FunctionStatusContainer",
)
status_registry.register(
    "container+job",
    "digitalhub_core_container.entities.tasks.status",
    "TaskStatusJob",
)
status_registry.register(
    "container+serve",
    "digitalhub_core_container.entities.tasks.status",
    "TaskStatusServe",
)
status_registry.register(
    "container+deploy",
    "digitalhub_core_container.entities.tasks.status",
    "TaskStatusDeploy",
)
status_registry.register(
    "container+run",
    "digitalhub_core_container.entities.runs.status",
    "RunStatusContainer",
)

spec_registry = SpecRegistry()
spec_registry.register(
    "container",
    "digitalhub_core_container.entities.functions.spec",
    "FunctionSpecContainer",
    "FunctionParamsContainer",
)
spec_registry.register(
    "container+job",
    "digitalhub_core_container.entities.tasks.spec",
    "TaskSpecJob",
    "TaskParamsJob",
)
spec_registry.register(
    "container+serve",
    "digitalhub_core_container.entities.tasks.spec",
    "TaskSpecServe",
    "TaskParamsServe",
)
spec_registry.register(
    "container+deploy",
    "digitalhub_core_container.entities.tasks.spec",
    "TaskSpecDeploy",
    "TaskParamsDeploy",
)
spec_registry.register(
    "container+run",
    "digitalhub_core_container.entities.runs.spec",
    "RunSpecContainer",
    "RunParamsContainer",
)
