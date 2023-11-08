from sdk.utils.modules_utils import ModuleRegistry

registry = ModuleRegistry()
registry.register_runtime("sdk_dbt.runtime.runtime", "RuntimeDBT")
registry.register_function("sdk_dbt.entities.functions.spec", "FunctionSpecDBT", "FunctionParamsDBT")
registry.register_tasks("transform", "sdk_dbt.entities.tasks.spec", "TaskSpecTransform", "TaskParamsTransform")
