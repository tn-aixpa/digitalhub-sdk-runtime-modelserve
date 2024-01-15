import pytest
from digitalhub_core.client.objects.local import ClientLocal
from digitalhub_core.utils.commons import FUNC, PROJ, RUNS


@pytest.fixture
def client():
    return ClientLocal()


def test_create_object(client, api_base, api_context):
    obj1 = {"name": "test"}
    api1 = api_base + f"/{PROJ}"
    result1 = client.create_object(obj1, api1)
    assert result1 == obj1

    obj2 = {"id": "test"}
    api2 = api_base + f"/{RUNS}"
    result2 = client.create_object(obj2, api2)
    assert result2 == obj2

    obj3 = {"id": "test", "name": "test"}
    api3 = api_context + f"/{FUNC}"
    result3 = client.create_object(obj3, api3)
    assert result3 == obj3
