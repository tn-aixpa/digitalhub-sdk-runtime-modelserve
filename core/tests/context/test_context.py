import pytest
from digitalhub_core.context.context import Context


@pytest.fixture(scope="session")
def context(project):
    return Context(project)


def test_create_object(context, api_context):
    obj = {"id": "1"}
    api = f"{api_context}/{context.name}/runs"
    assert context.create_object(obj, api) == obj

    obj = {"name": "test", "id": "1"}
    api = f"{api_context}/{context.name}/artifacts"
    assert context.create_object(obj, api) == obj


def test_read_object(context, api_context):
    obj = {"id": "2"}
    api = f"{api_context}/{context.name}/runs"
    context.create_object(obj, api)
    api = f"{api_context}/{context.name}/runs/2"
    assert context.read_object(api) == obj

    obj = {"name": "test", "id": "2"}
    api = f"{api_context}/{context.name}/artifacts"
    context.create_object(obj, api)
    api = f"{api_context}/{context.name}/artifacts/test/2"
    assert context.read_object(api) == obj


def test_update_object(context, api_context):
    obj = {"id": "3"}
    api = f"{api_context}/{context.name}/runs"
    context.create_object(obj, api)
    updated_obj = {"id": "3", "updated": True}
    api = f"{api_context}/{context.name}/runs/3"
    assert context.update_object(updated_obj, api) == updated_obj

    obj = {"name": "test", "id": "3"}
    api = f"{api_context}/{context.name}/artifacts"
    context.create_object(obj, api)
    updated_obj = {"name": "test", "id": "3", "updated": True}
    api = f"{api_context}/{context.name}/artifacts/test/3"
    assert context.update_object(updated_obj, api) == updated_obj


def test_delete_object(context, api_context):
    obj = {"id": "4"}
    api = f"{api_context}/{context.name}/runs"
    context.create_object(obj, api)
    api = f"{api_context}/{context.name}/runs/4?cascade=false"
    assert context.delete_object(api) == {'deleted': {'id': '4'}}

    obj = {"name": "test", "id": "4"}
    api = f"{api_context}/{context.name}/artifacts"
    context.create_object(obj, api)
    api = f"{api_context}/{context.name}/artifacts/test/4?cascade=false"
    assert context.delete_object(api) == {'deleted': {'id': '4', 'name': 'test'}}
