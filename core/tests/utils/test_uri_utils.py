import pytest
from oltreai_core.utils.uri_utils import map_uri_scheme


@pytest.mark.parametrize(
    "uri,expected_scheme",
    [
        ("file://path/to/file", "local"),
        ("local://path/to/file", "local"),
        ("/path/to/file", "local"),
        ("http://example.com", "remote"),
        ("https://example.com", "remote"),
        ("remote://example.com", "remote"),
        ("s3://bucket/key", "s3"),
        ("s3a://bucket/key", "s3"),
        ("s3n://bucket/key", "s3"),
        ("sql://database/table", "sql"),
        ("postgresql://database/table", "sql"),
    ],
)
def test_map_uri_scheme(uri, expected_scheme):
    assert map_uri_scheme(uri) == expected_scheme


def test_map_uri_scheme_unknown():
    with pytest.raises(ValueError):
        map_uri_scheme("unknown://path/to/file")
