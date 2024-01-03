from digitalhub_core.utils.modules_utils import FUNC, ModuleRegistry, Obj, Rtm


def test_module_registry():
    registry = ModuleRegistry()

    # Test register_runtime
    registry.register_runtime("module1", "RuntimeClass1")
    assert isinstance(registry.get_runtime(), Rtm)
    assert registry.get_runtime().module == "module1"
    assert registry.get_runtime().class_name == "RuntimeClass1"

    # Test register_function
    registry.register_function("module2", "FunctionSpecClass2", "FunctionParamsClass2")
    assert isinstance(registry.get_spec(FUNC), Obj)
    assert registry.get_spec(FUNC).module == "module2"
    assert registry.get_spec(FUNC).class_spec == "FunctionSpecClass2"
    assert registry.get_spec(FUNC).class_params == "FunctionParamsClass2"

    # Test register_tasks and get_spec
    registry.register_tasks("kind3", "module3", "TaskSpecClass3", "TaskParamsClass3")
    assert isinstance(registry.get_spec("tasks", "kind3"), Obj)
    assert registry.get_spec("tasks", "kind3").module == "module3"
    assert registry.get_spec("tasks", "kind3").class_spec == "TaskSpecClass3"
    assert registry.get_spec("tasks", "kind3").class_params == "TaskParamsClass3"
