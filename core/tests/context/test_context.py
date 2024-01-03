import pytest
from digitalhub_core.context.context import Context
from digitalhub_core.entities.projects.crud import get_or_create_project


@pytest.fixture(autouse=True, scope="session")
def project():
    return get_or_create_project(name="test-project", local=True)


@pytest.fixture(autouse=True, scope="session")
def context(project):
    return Context(project)


def test_create_object(context):
    obj = {"name": "test", "id": "1"}
    api = "/api/v1/runs"
    assert context.create_object(obj, api) == obj


def test_read_object(context):
    obj = {"name": "test", "id": "2"}
    api = "/api/v1/runs"
    context.create_object(obj, api)
    api = "/api/v1/runs/2"
    assert context.read_object(api) == obj


def test_update_object(context):
    obj = {"name": "test", "id": "3"}
    api = "/api/v1/runs"
    context.create_object(obj, api)
    updated_obj = {"name": "test", "id": "3", "updated": True}
    api = "/api/v1/runs/test"
    assert context.update_object(updated_obj, api) == updated_obj


def test_delete_object(context):
    obj = {"name": "test", "id": "4"}
    api = "/api/v1/runs"
    context.create_object(obj, api)
    api = "/api/v1/runs/4?cascade=false"
    assert context.delete_object(api) == {"deleted": obj}
