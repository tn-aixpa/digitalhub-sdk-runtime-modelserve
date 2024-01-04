from digitalhub_core.utils.modules_utils import ModuleRegistry

registry = ModuleRegistry()
registry.register_runtime(
    "digitalhub_data_dbt.runtime.runtime",
    "RuntimeDBT",
)
registry.register_function(
    "digitalhub_data_dbt.entities.functions.spec",
    "FunctionSpecDBT",
    "FunctionParamsDBT",
)
registry.register_tasks(
    "transform",
    "digitalhub_data_dbt.entities.tasks.spec",
    "TaskSpecTransform",
    "TaskParamsTransform",
)
