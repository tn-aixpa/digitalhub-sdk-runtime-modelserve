import pytest


@pytest.fixture
def api_base():
    return "/api/v1"


@pytest.fixture
def api_context():
    return "/api/v1/-"
