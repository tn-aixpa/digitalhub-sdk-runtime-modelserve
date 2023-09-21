"""
Run specification registry module.
"""
from sdk.entities.run.kinds import RunKinds
from sdk.entities.run.spec.models import RunParams
from sdk.entities.run.spec.objects import RunSpecRun

REGISTRY_SPEC = {
    RunKinds.RUN.value: RunSpecRun,
}
REGISTRY_MODEL = {
    RunKinds.RUN.value: RunParams,
}
