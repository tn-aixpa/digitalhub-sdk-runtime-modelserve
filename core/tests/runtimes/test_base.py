import pytest
from digitalhub_core.runtimes.base import Runtime


@pytest.fixture
def runtime():
    return Runtime()


def test_get_action(runtime):
    run = {"spec": {"task": "project+action://name:version"}}
    assert runtime._get_action(run) == "action"
