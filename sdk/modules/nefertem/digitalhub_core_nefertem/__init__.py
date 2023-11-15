from digitalhub_core.utils.modules_utils import ModuleRegistry

registry = ModuleRegistry()
registry.register_runtime("digitalhub_core_nefertem.runtime.runtime", "RuntimeNefertem")
registry.register_function(
    "digitalhub_core_nefertem.entities.functions.spec", "FunctionSpecNefertem", "FunctionParamsNefertem"
)
registry.register_tasks("infer", "digitalhub_core_nefertem.entities.tasks.spec", "TaskSpecInfer", "TaskParamsInfer")
registry.register_tasks(
    "profile", "digitalhub_core_nefertem.entities.tasks.spec", "TaskSpecProfile", "TaskParamsProfile"
)
registry.register_tasks(
    "validate", "digitalhub_core_nefertem.entities.tasks.spec", "TaskSpecValidate", "TaskParamsValidate"
)
registry.register_tasks("metric", "digitalhub_core_nefertem.entities.tasks.spec", "TaskSpecMetric", "TaskParamsMetric")
