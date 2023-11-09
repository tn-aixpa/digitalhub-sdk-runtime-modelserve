from sdk.utils.modules_utils import ModuleRegistry

registry = ModuleRegistry()
registry.register_runtime("sdk_nefertem.runtime.runtime", "RuntimeNefertem")
registry.register_function("sdk_nefertem.entities.functions.spec", "FunctionSpecNefertem", "FunctionParamsNefertem")
registry.register_tasks("infer", "sdk_nefertem.entities.tasks.spec", "TaskSpecInfer", "TaskParamsInfer")
registry.register_tasks("profile", "sdk_nefertem.entities.tasks.spec", "TaskSpecProfile", "TaskParamsProfile")
registry.register_tasks("validate", "sdk_nefertem.entities.tasks.spec", "TaskSpecValidate", "TaskParamsValidate")
registry.register_tasks("metric", "sdk_nefertem.entities.tasks.spec", "TaskSpecMetric", "TaskParamsMetric")
