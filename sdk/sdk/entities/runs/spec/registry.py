"""
Run specification registry module.
"""
from sdk.entities.runs.kinds import RunKinds
from sdk.entities.runs.spec.models import RunParams
from sdk.entities.runs.spec.objects import RunSpecRun

RUN_SPEC = {
    RunKinds.RUN.value: RunSpecRun,
}
RUN_MODEL = {
    RunKinds.RUN.value: RunParams,
}
