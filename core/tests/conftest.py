import pytest
from digitalhub_core.context.context import Context
from digitalhub_core.entities.project.crud import delete_project, get_or_create_project


@pytest.fixture
def api_base():
    return "/api/v1"


@pytest.fixture
def api_context():
    return "/api/v1/-"


@pytest.fixture(scope="session")
def project():
    yield get_or_create_project(name="test", local=True)
    try:
        delete_project(name="test")
    except Exception:
        pass


@pytest.fixture(scope="session")
def context(project):
    return Context(project)
