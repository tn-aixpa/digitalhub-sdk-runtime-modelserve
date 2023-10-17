"""
Run specification registry module.
"""
from sdk.entities.base.spec import SpecRegistry
from sdk.entities.runs.kinds import RunKinds
from sdk.entities.runs.spec.objects.run import RunParamsRun, RunSpecRun

run_registry = SpecRegistry()
run_registry.register(RunKinds.RUN.value, RunSpecRun, RunParamsRun)
