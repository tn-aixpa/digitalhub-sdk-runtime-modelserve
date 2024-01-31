import pytest
from digitalhub_core.client.objects.local import ClientLocal

FUNC = "functions"
PROJ = "projects"
RUNS = "runs"


@pytest.fixture
def client():
    return ClientLocal()


def test_create_object(client, api_base, api_context):
    obj1 = {"name": "test"}
    api1 = f"{api_base}/{PROJ}"
    result1 = client.create_object(obj1, api1)
    assert result1 == obj1

    obj2 = {"id": "test"}
    api2 = f"{api_base}/{RUNS}"
    result2 = client.create_object(obj2, api2)
    assert result2 == obj2

    obj3 = {"id": "test", "name": "test"}
    api3 = f"{api_context}/{FUNC}"
    result3 = client.create_object(obj3, api3)
    assert result3 == obj3


def test_read_object(client, api_base, api_context):
    expected_result = {"name": "test"}
    client._db.setdefault(PROJ, {}).setdefault("test", expected_result)
    api = f"{api_base}/{PROJ}/test"
    actual_result = client.read_object(api)
    assert actual_result == expected_result

    expected_result = {"id": "test", "name": "test"}
    client._db.setdefault(FUNC, {}).setdefault("test", {}).setdefault("test", expected_result)
    api = f"{api_context}/test/{FUNC}/test/test"
    actual_result = client.read_object(api)
    assert actual_result == expected_result
