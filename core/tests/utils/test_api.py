import pytest
from digitalhub_core.utils.api import (
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
    "proj,dto,name,uuid,expected",
    [
        ("project1", "dto1", "name1", "uuid1", "/api/v1/-/project1/dto1/name1/uuid1"),
        ("project2", "dto2", "name2", None, "/api/v1/-/project2/dto2/name2/latest"),
    ],
)
def test_api_ctx_read(proj, dto, name, uuid, expected):
    assert api_ctx_read(proj, dto, name, uuid) == expected


@pytest.mark.parametrize(
    "proj,dto,name,uuid,expected",
    [
        ("project1", "dto1", "name1", "uuid1", "/api/v1/-/project1/dto1/name1/uuid1"),
        ("project2", "dto2", "name2", "uuid2", "/api/v1/-/project2/dto2/name2/uuid2"),
    ],
)
def test_api_ctx_update(proj, dto, name, uuid, expected):
    assert api_ctx_update(proj, dto, name, uuid) == expected


@pytest.mark.parametrize(
    "proj,dto,name,uuid,expected",
    [
        ("project1", "dto1", "name1", "uuid1", "/api/v1/-/project1/dto1/name1/uuid1?cascade=true"),
        ("project2", "dto2", "name2", None, "/api/v1/-/project2/dto2/name2?cascade=true"),
    ],
)
def test_api_ctx_delete(proj, dto, name, uuid, expected):
    assert api_ctx_delete(proj, dto, name, uuid) == expected


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
    "dto,name,expected",
    [
        ("dto1", "name1", "/api/v1/dto1/name1"),
        ("dto2", "name2", "/api/v1/dto2/name2"),
    ],
)
def test_api_base_read(dto, name, expected):
    assert api_base_read(dto, name) == expected


@pytest.mark.parametrize(
    "dto,name,expected",
    [
        ("dto1", "name1", "/api/v1/dto1/name1"),
        ("dto2", "name2", "/api/v1/dto2/name2"),
    ],
)
def test_api_base_update(dto, name, expected):
    assert api_base_update(dto, name) == expected


@pytest.mark.parametrize(
    "dto,name,cascade,expected",
    [
        ("dto1", "name1", True, "/api/v1/dto1/name1?cascade=true"),
        ("dto2", "name2", False, "/api/v1/dto2/name2?cascade=false"),
    ],
)
def test_api_base_delete(dto, name, cascade, expected):
    assert api_base_delete(dto, name, cascade) == expected
