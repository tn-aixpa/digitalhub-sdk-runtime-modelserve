"""
Function specification registry module.
"""
from sdk.entities.function.kinds import FunctionKinds
from sdk.entities.function.spec.models import FunctionParamsDBT, FunctionParamsMLRun
from sdk.entities.function.spec.objects import FunctionSpecDBT, FunctionSpecMLRun

REGISTRY_SPEC = {
    FunctionKinds.MLRUN.value: FunctionSpecMLRun,
    FunctionKinds.DBT.value: FunctionSpecDBT,
}
REGISTRY_MODEL = {
    FunctionKinds.MLRUN.value: FunctionParamsMLRun,
    FunctionKinds.DBT.value: FunctionParamsDBT,
}
