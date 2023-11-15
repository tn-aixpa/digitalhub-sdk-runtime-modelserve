from digitalhub_core.utils.modules_utils import ModuleRegistry

registry = ModuleRegistry()
registry.register_runtime("digitalhub_core_dbt.runtime.runtime", "RuntimeDBT")
registry.register_function("digitalhub_core_dbt.entities.functions.spec", "FunctionSpecDBT", "FunctionParamsDBT")
registry.register_tasks(
    "transform", "digitalhub_core_dbt.entities.tasks.spec", "TaskSpecTransform", "TaskParamsTransform"
)
