from sdk.entities.function.kinds import FunctionKinds
from sdk.entities.task.kinds import TaskKinds

REGISTRY_RUNTIMES = {}
try:
    from sdk.runtimes.objects.dbt import RuntimeJobDBT

    REGISTRY_RUNTIMES[FunctionKinds.DBT.value] = {
        TaskKinds.JOB.value: RuntimeJobDBT,
    }
except ImportError:
    ...
