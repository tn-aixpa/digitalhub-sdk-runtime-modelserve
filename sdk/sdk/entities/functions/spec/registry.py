"""
Function specification registry module.
"""
from sdk.entities.base.spec import SpecRegistry
from sdk.entities.functions.kinds import FunctionKinds
from sdk.entities.functions.spec.objects.dbt import FunctionParamsDBT, FunctionSpecDBT
from sdk.entities.functions.spec.objects.mlrun import FunctionParamsMLRun, FunctionSpecMLRun
from sdk.entities.functions.spec.objects.nefertem import FunctionParamsNefertem, FunctionSpecNefertem
from sdk.entities.functions.spec.objects.python import FunctionParamsPython, FunctionSpecPython

function_registry = SpecRegistry()
function_registry.register(FunctionKinds.PYTHON.value, FunctionSpecPython, FunctionParamsPython)
function_registry.register(FunctionKinds.MLRUN.value, FunctionSpecMLRun, FunctionParamsMLRun)
function_registry.register(FunctionKinds.DBT.value, FunctionSpecDBT, FunctionParamsDBT)
function_registry.register(FunctionKinds.NEFERTEM.value, FunctionSpecNefertem, FunctionParamsNefertem)
