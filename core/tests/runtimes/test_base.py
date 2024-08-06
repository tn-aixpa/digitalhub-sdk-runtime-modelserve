import pytest
from digitalhub_core.runtimes.base import Runtime


class MockRuntime(Runtime):
    allowed_actions = ["action"]


@pytest.fixture
def runtime():
    return MockRuntime()


def test_get_action(runtime):
    runtime.allowed_actions = ["action"]
    run = {"spec": {"task": "project+action://name:version"}}
    assert runtime._get_action(run) == "action"
