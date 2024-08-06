import pytest
from oltreai_core.entities._base.api import (
    api_base_create,
    api_base_delete,
    api_base_read,
    api_base_update,
    api_ctx_create,
    api_ctx_delete,
    api_ctx_read,
    api_ctx_update,
)


@pytest.mark.parametrize(
    "proj,dto,expected",
    [
        ("project1", "dto1", "/api/v1/-/project1/dto1"),
        ("project2", "dto2", "/api/v1/-/project2/dto2"),
    ],
)
def test_api_ctx_create(proj, dto, expected):
    assert api_ctx_create(proj, dto) == expected


@pytest.mark.parametrize(
    "proj,dto,uuid,expected",
    [
        ("project1", "dto1", "uuid1", "/api/v1/-/project1/dto1/uuid1"),
        ("project2", "dto2", "uuid2", "/api/v1/-/project2/dto2/uuid2"),
    ],
)
def test_api_ctx_read(proj, dto, uuid, expected):
    assert api_ctx_read(proj, dto, uuid) == expected


@pytest.mark.parametrize(
    "proj,dto,uuid,expected",
    [
        ("project1", "dto1", "uuid1", "/api/v1/-/project1/dto1/uuid1"),
        ("project2", "dto2", "uuid2", "/api/v1/-/project2/dto2/uuid2"),
    ],
)
def test_api_ctx_update(proj, dto, uuid, expected):
    assert api_ctx_update(proj, dto, uuid) == expected


@pytest.mark.parametrize(
    "proj,dto,uuid,expected",
    [
        ("project1", "dto1", "uuid1", "/api/v1/-/project1/dto1/uuid1"),
        ("project2", "dto2", "uuid2", "/api/v1/-/project2/dto2/uuid2"),
    ],
)
def test_api_ctx_delete(proj, dto, uuid, expected):
    assert api_ctx_delete(proj, dto, uuid) == expected


@pytest.mark.parametrize(
    "dto,expected",
    [
        ("dto1", "/api/v1/dto1"),
        ("dto2", "/api/v1/dto2"),
    ],
)
def test_api_base_create(dto, expected):
    assert api_base_create(dto) == expected


@pytest.mark.parametrize(
    "dto,uuid,expected",
    [
        ("dto1", "uuid1", "/api/v1/dto1/uuid1"),
        ("dto2", "uuid2", "/api/v1/dto2/uuid2"),
    ],
)
def test_api_base_read(dto, uuid, expected):
    assert api_base_read(dto, uuid) == expected


@pytest.mark.parametrize(
    "dto,uuid,expected",
    [
        ("dto1", "uuid1", "/api/v1/dto1/uuid1"),
        ("dto2", "uuid2", "/api/v1/dto2/uuid2"),
    ],
)
def test_api_base_update(dto, uuid, expected):
    assert api_base_update(dto, uuid) == expected


@pytest.mark.parametrize(
    "dto,uuid,expected",
    [
        ("dto1", "uuid1", "/api/v1/dto1/uuid1"),
        ("dto2", "uuid2", "/api/v1/dto2/uuid2"),
    ],
)
def test_api_base_delete(dto, uuid, expected):
    assert api_base_delete(dto, uuid) == expected
