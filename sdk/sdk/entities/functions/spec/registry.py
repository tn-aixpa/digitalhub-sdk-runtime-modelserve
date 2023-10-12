"""
Function specification registry module.
"""
from sdk.entities.functions.kinds import FunctionKinds
from sdk.entities.functions.spec.objects.dbt import (
    FunctionParamsDBT,
    FunctionSpecDBT,
)
from sdk.entities.functions.spec.objects.mlrun import (
    FunctionParamsMLRun,
    FunctionSpecMLRun,
)

FUNCTION_SPEC = {
    FunctionKinds.MLRUN.value: FunctionSpecMLRun,
    FunctionKinds.DBT.value: FunctionSpecDBT,
}
FUNCTION_MODEL = {
    FunctionKinds.MLRUN.value: FunctionParamsMLRun,
    FunctionKinds.DBT.value: FunctionParamsDBT,
}
