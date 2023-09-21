"""
Function specification registry module.
"""
from sdk.entities.function.kinds import FunctionKinds
from sdk.entities.function.spec.models import FunctionParamsDBT, FunctionParamsJob
from sdk.entities.function.spec.objects import FunctionSpecDBT, FunctionSpecJob

REGISTRY_SPEC = {
    FunctionKinds.JOB.value: FunctionSpecJob,
    FunctionKinds.DBT.value: FunctionSpecDBT,
}
REGISTRY_MODEL = {
    FunctionKinds.JOB.value: FunctionParamsJob,
    FunctionKinds.DBT.value: FunctionParamsDBT,
}
