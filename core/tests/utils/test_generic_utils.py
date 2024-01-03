import pytest
from digitalhub_core.utils.generic_utils import build_uuid, decode_string, encode_string, parse_entity_key


@pytest.mark.parametrize(
    "uuid_input,expected",
    [
        ("123e4567-e89b-12d3-a456-426614174000", "123e4567-e89b-12d3-a456-426614174000"),
        (None, None),
    ],
)
def test_build_uuid(uuid_input, expected):
    if expected is None:
        assert isinstance(build_uuid(uuid_input), str)
    else:
        assert build_uuid(uuid_input) == expected


@pytest.mark.parametrize(
    "string,expected",
    [
        ("SGVsbG8gd29ybGQ=", "Hello world"),
        ("", ""),
    ],
)
def test_decode_string(string, expected):
    assert decode_string(string) == expected


@pytest.mark.parametrize(
    "string,expected",
    [
        ("Hello world", "SGVsbG8gd29ybGQ="),
        ("", ""),
    ],
)
def test_encode_string(string, expected):
    assert encode_string(string) == expected


@pytest.mark.parametrize(
    "key,expected",
    [
        (
            "store://project/name:123e4567-e89b-12d3-a456-426614174000",
            ("project", "name", "123e4567-e89b-12d3-a456-426614174000"),
        ),
        ("store://project/name", ValueError),
    ],
)
def test_parse_entity_key(key, expected):
    if isinstance(expected, tuple):
        assert parse_entity_key(key) == expected
    else:
        with pytest.raises(expected):
            parse_entity_key(key)
