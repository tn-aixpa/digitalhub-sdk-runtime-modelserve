from unittest.mock import patch

import pandas as pd
import pytest
from digitalhub_core.stores.objects.remote import RemoteStore, RemoteStoreConfig


@pytest.fixture
def remote_store():
    config = RemoteStoreConfig()
    return RemoteStore("test_store", "remote", config)


def test_init(remote_store):
    assert remote_store.name == "test_store"
    assert remote_store.type == "remote"


@patch("digitalhub_core.stores.objects.remote.RemoteStore._download_file")
def test_download(mock_download_file, remote_store):
    mock_download_file.return_value = "dst.csv"
    assert remote_store.download("http://test.com/src.csv", "dst.csv") == "dst.csv"
    mock_download_file.assert_called_once_with("http://test.com/src.csv", "dst.csv")


@patch("digitalhub_core.stores.objects.remote.RemoteStore._download_file")
def test_fetch_artifact(mock_download_file, remote_store):
    mock_download_file.return_value = "dst.csv"
    assert remote_store.fetch_artifact("http://test.com/src.csv", "dst.csv") == "dst.csv"
    mock_download_file.assert_called_once_with("http://test.com/src.csv", "dst.csv")


def test_upload_raises_not_implemented_error(remote_store):
    with pytest.raises(NotImplementedError):
        remote_store.upload("src", "dst")


def test_persist_artifact_raises_not_implemented_error(remote_store):
    with pytest.raises(NotImplementedError):
        remote_store.persist_artifact("src", "dst")


def test_write_df_raises_not_implemented_error(remote_store):
    with pytest.raises(NotImplementedError):
        remote_store.write_df(pd.DataFrame(), "dst")


def test_is_local(remote_store):
    assert not remote_store.is_local()
