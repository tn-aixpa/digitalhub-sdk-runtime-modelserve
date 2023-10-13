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
from sdk.entities.functions.spec.objects.python import (
    FunctionParamsPython,
    FunctionSpecPython,
)

FUNCTION_SPEC = {
    FunctionKinds.MLRUN.value: FunctionSpecMLRun,
    FunctionKinds.DBT.value: FunctionSpecDBT,
    FunctionKinds.NEFERTEM.value: FunctionSpecNefertem,
    FunctionKinds.PYTHON.value: FunctionSpecPython,
}
FUNCTION_MODEL = {
    FunctionKinds.MLRUN.value: FunctionParamsMLRun,
    FunctionKinds.DBT.value: FunctionParamsDBT,
    FunctionKinds.NEFERTEM.value: FunctionParamsNefertem,
    FunctionKinds.PYTHON.value: FunctionParamsPython,
}
