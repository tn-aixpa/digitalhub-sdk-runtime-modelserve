import pytest
import pandas as pd
from unittest.mock import patch
from digitalhub_core.stores.objects.local import LocalStore, LocalStoreConfig

@pytest.fixture
def local_store():
    config = LocalStoreConfig(path="/tmp")
    return LocalStore("test_store", "local", config)

def test_init(local_store):
    assert local_store.name == "test_store"
    assert local_store.type == "local"
    assert local_store.config.path == "/tmp"

def test_download_raises_not_implemented_error(local_store):
    with pytest.raises(NotImplementedError):
        local_store.download("src", "dst")

def test_upload_raises_not_implemented_error(local_store):
    with pytest.raises(NotImplementedError):
        local_store.upload("src", "dst")

@patch("shutil.copy")
def test_fetch_artifact(mock_copy, local_store):
    assert local_store.fetch_artifact("src") == "src"
    mock_copy.return_value = "dst"
    assert local_store.fetch_artifact("src", "dst") == "dst"
    mock_copy.assert_called_once_with("src", "dst")

@patch("shutil.copy")
def test_persist_artifact(mock_copy, local_store):
    mock_copy.return_value = "dst"
    assert local_store.persist_artifact("src", "dst") == "dst"
    mock_copy.assert_called_once_with("src", "dst")

@patch("pandas.DataFrame.to_parquet")
def test_write_df(mock_to_parquet, local_store):
    df = pd.DataFrame({"A": [1, 2, 3]})
    local_store.write_df(df, "/tmp/data.parquet")
    mock_to_parquet.assert_called_once_with("/tmp/data.parquet", index=False)

def test_is_local(local_store):
    assert local_store.is_local() == True
