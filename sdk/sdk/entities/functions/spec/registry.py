"""
Function specification registry module.
"""
from sdk.entities.functions.kinds import FunctionKinds
from sdk.entities.functions.spec.objects.dbt import FunctionParamsDBT, FunctionSpecDBT
from sdk.entities.functions.spec.objects.mlrun import (
    FunctionParamsMLRun,
    FunctionSpecMLRun,
)
from sdk.entities.functions.spec.objects.nefertem import (
    FunctionParamsNefertem,
    FunctionSpecNefertem,
)

FUNCTION_SPEC = {
    FunctionKinds.MLRUN.value: FunctionSpecMLRun,
    FunctionKinds.DBT.value: FunctionSpecDBT,
    FunctionKinds.NEFERTEM.value: FunctionSpecNefertem,
}
FUNCTION_MODEL = {
    FunctionKinds.MLRUN.value: FunctionParamsMLRun,
    FunctionKinds.DBT.value: FunctionParamsDBT,
    FunctionKinds.NEFERTEM.value: FunctionParamsNefertem,
}
