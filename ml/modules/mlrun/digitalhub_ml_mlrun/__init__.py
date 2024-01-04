from digitalhub_core.utils.modules_utils import ModuleRegistry

registry = ModuleRegistry()
registry.register_runtime(
    "digitalhub_ml_mlrun.runtime.runtime",
    "RuntimeMLRun",
)
registry.register_function(
    "digitalhub_ml_mlrun.entities.functions.spec",
    "FunctionSpecMLRun",
    "FunctionParamsMLRun",
)
registry.register_tasks(
    "mlrun",
    "digitalhub_ml_mlrun.entities.tasks.spec",
    "TaskSpecMLRun",
    "TaskParamsMLRun",
)
