"""
Function specification registry module.
"""
from sdk.entities.functions.kinds import FunctionKinds
from sdk.entities.functions.spec.models import FunctionParamsDBT, FunctionParamsMLRun
from sdk.entities.functions.spec.objects import FunctionSpecDBT, FunctionSpecMLRun

FUNCTION_SPEC = {
    FunctionKinds.MLRUN.value: FunctionSpecMLRun,
    FunctionKinds.DBT.value: FunctionSpecDBT,
}
FUNCTION_MODEL = {
    FunctionKinds.MLRUN.value: FunctionParamsMLRun,
    FunctionKinds.DBT.value: FunctionParamsDBT,
}
