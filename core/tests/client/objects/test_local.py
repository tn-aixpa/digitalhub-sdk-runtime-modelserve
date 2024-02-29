import pytest
from digitalhub_core.client.objects.local import ClientLocal
from digitalhub_core.utils.exceptions import BackendError

ARTF = "artifacts"
WKFL = "workflows"
FUNC = "functions"
PROJ = "projects"
RUNS = "runs"
TASK = "tasks"


@pytest.fixture
def client():
    return ClientLocal()


def test_create_object(client, api_base, api_context):
    obj = {"name": "test"}
    api = f"{api_base}/{PROJ}"
    result = client.create_object(obj, api)
    assert result == obj
    with pytest.raises(BackendError):
        client.create_object(obj, api)

    for i in [TASK, RUNS]:
        obj = {"id": "test"}
        api = f"{api_context}/test/{i}"
        result = client.create_object(obj, api)
        assert result == obj
        obj = {"id": "test2", "name": "test"}
        result = client.create_object(obj, api)
        assert result == obj

    for i in [ARTF, WKFL, FUNC, "generic"]:
        obj = {"id": "test", "name": "test"}
        api = f"{api_context}/test/{FUNC}"
        result = client.create_object(obj, api)
        assert result == obj
        obj = {"id": "test2", "name": "test"}
        result = client.create_object(obj, api)
        assert result == obj


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
