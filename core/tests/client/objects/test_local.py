import pytest
from digitalhub_core.client.objects.local import ClientLocal
from digitalhub_core.utils.exceptions import BackendError


@pytest.fixture
def client():
    return ClientLocal()


@pytest.fixture
def api_base():
    return "/api/v1"


@pytest.fixture
def api_context():
    return "/api/v1/-"
