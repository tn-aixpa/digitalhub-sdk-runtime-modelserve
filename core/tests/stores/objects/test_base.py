from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest
from digitalhub_core.stores.objects.base import Store
from digitalhub_core.utils.exceptions import StoreError


class TestStore(Store):
    def download(self, src: str, dst: str | None = None) -> str:
        ...

    def fetch_artifact(self, src: str, dst: str | None = None) -> str:
        ...

    def upload(self, src: str, dst: str | None = None) -> str:
        ...

    def persist_artifact(self, src: str, dst: str | None = None) -> str:
        ...

    def write_df(self, df: pd.DataFrame, dst: str | None = None, **kwargs) -> str:
        ...

    def is_local(self) -> bool:
        ...


@pytest.fixture
def store():
    return TestStore("store1", "type1")


def test_init(store):
    assert store.name == "store1"
    assert store.type == "type1"
    assert store._registry == {}


def test_check_local_dst(store):
    with patch("digitalhub_core.stores.objects.base.map_uri_scheme", return_value="local"), patch(
        "digitalhub_core.stores.objects.base.Store._build_path"
    ) as mock_build_path:
        store._check_local_dst("local_path")
        mock_build_path.assert_called_once_with("local_path")


def test_check_local_dst_not_local(store):
    with patch("digitalhub_core.stores.objects.base.map_uri_scheme", return_value="not_local"):
        with pytest.raises(StoreError, match="Destination 'not_local_path' is not a local path."):
            store._check_local_dst("not_local_path")


def test_build_path():
    path = "/tmp/test_subdir"
    Store._build_path(path)
    assert Path(path).exists()
    os.rmdir(path)


def test_build_temp(store):
    with patch("digitalhub_core.stores.objects.base.mkdtemp", return_value="tmp_dir"):
        temp_path = store._build_temp("src_file")
        assert temp_path == "tmp_dir/src_file"
        assert store._registry["src_file"] == "tmp_dir/src_file"


def test_read_df_csv(tmp_path):
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    csv_file = tmp_path / "data.csv"
    df.to_csv(csv_file, index=False)
    read_df = Store.read_df(csv_file, "csv")
    pd.testing.assert_frame_equal(read_df, df)


def test_read_df_parquet(tmp_path):
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    parquet_file = tmp_path / "data.parquet"
    df.to_parquet(parquet_file)
    read_df = Store.read_df(parquet_file, "parquet")
    pd.testing.assert_frame_equal(read_df, df)


def test_read_df_not_supported():
    with pytest.raises(ValueError, match="Format txt not supported."):
        Store.read_df("data.txt", "txt")
